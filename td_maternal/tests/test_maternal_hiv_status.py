from dateutil.relativedelta import relativedelta
from model_mommy import mommy

from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NO, NEG, NOT_APPLICABLE, UNK, IND
from edc_metadata.models import RequisitionMetadata

from td.models import Appointment

from ..maternal_hiv_status import MaternalHivStatus

from .mixins import PosMotherMixin, NegMotherMixin, AntenatalVisitsMotherMixin, DeliverMotherMixin, AddVisitInfantMixin


class TestMaternalHivStatusPos(DeliverMotherMixin, AntenatalVisitsMotherMixin, PosMotherMixin, TestCase):
    """Tests where the mother is POS."""

    def setUp(self):
        super(TestMaternalHivStatusPos, self).setUp()
        self.add_maternal_visits('2000M', '2010M')

    def test_pos_status_anytime(self):
        """Asserts can determine POS at any visit."""
        maternal_visit = self.add_maternal_visit('1010M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, POS)
        maternal_visit = self.add_maternal_visit('2000M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, POS)
        maternal_visit = self.add_maternal_visit('2010M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, POS)
        maternal_visit = self.add_maternal_visit('2020M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, POS)

    def test_dnapcr_for_exposed_infant(self):
        """Asserts that DNA PCR requisition is made available for an HIV exposed infant.
        """
        self.add_infant_visits('2000', '2010')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status='REQUIRED',
                model='td_lab.infantrequisition',
                panel_name='DNA PCR',
                visit_code='2010').count(), 1)


class TestMaternalHivStatusNeg(DeliverMotherMixin, AntenatalVisitsMotherMixin, AddVisitInfantMixin,
                               NegMotherMixin, TestCase):

    def test_neg_status_anytime(self):
        """Asserts can determine NEG at any visit."""
        maternal_visit = self.add_maternal_visit('1010M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        maternal_visit = self.add_maternal_visit('2000M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        maternal_visit = self.add_maternal_visit('2010M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        maternal_visit = self.add_maternal_visit('2020M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)

    def test_dnapcr_for_non_heu_infant(self):
        """test that for a NON HEU infant, then the DNA PCR requisition is NOT made available."""
        self.add_infant_visits('2000', '2010')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status='NOT_REQUIRED',
                model='td_lab.infantrequisition',
                panel_name='DNA PCR',
                visit_code='2010').count(), 1)

    def test_ind_status_from_rapid_test(self):
        """test that we can figure out a posetive status taking in to consideration rapid tests."""
        self.add_maternal_visits('1020M', '2000M', '2010M')
        maternal_visit = self.get_maternal_visit('2010M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        self.add_maternal_visits('2020M', '2060M')
        mommy.make_recipe('td_maternal.rapidtestresult', maternal_visit=maternal_visit, result=IND)
        maternal_visit = self.get_maternal_visit('2060M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, IND)

    def test_neg_status_from_enrollment(self):
        """test that we can figure out a negative status with just the enrollment status."""
        for code in ['1020M', '2000M', '2010M', '2020M']:
            maternal_visit = self.add_maternal_visit(code)
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)

    def test_neg_status_from_rapid_test(self):
        """test that we can figure out a negative status taking in to consideration rapid tests."""
        self.add_maternal_visits('1020M', '2000M', '2010M')
        maternal_visit = self.get_maternal_visit('2010')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        mommy.make_recipe('td_maternal.rapidtestresult', maternal_visit=maternal_visit, result=NEG)
        # Visit within 3months of rapid test.
        maternal_visit = self.add_maternal_visit('2020')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)

    def test_unkown_status(self):
        """test that a negative result that is more than 3months old will lead to UNK status."""
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code='1020M')
        mommy.make_recipe('td_maternal.maternallabdel', registered_subject=self.registered_subject)
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code='2000M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code='2010M')
        maternal_visit_2010M = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=maternal_visit_2010M.subject_identifier,
            reference_datetime=maternal_visit_2010M.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        mommy.make_recipe(
            'td_maternal.rapidtestresult', maternal_visit=maternal_visit_2010M,
            result_date=(get_utcnow() - relativedelta(months=4)).date(),
            result=NEG)
        # Visit within 3months of rapid test.
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code='2020M')
        maternal_visit_2020M = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=maternal_visit_2020M.subject_identifier,
            reference_datetime=maternal_visit_2020M.report_datetime)
        self.assertEqual(maternal_hiv_status.result, UNK)


class TestMaternalHivStatusWithForm(TestCase):

    def test_valid_hiv_neg_week32_test_date(self):
        """Test that NEG status is valid for week32_test_date"""
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': NEG,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (get_utcnow() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': NO,
                   'rapid_test_date': None,
                   'rapid_test_result': None,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=34)).date()}
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = mommy.make_recipe('td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000, number_of_gestations=1,)
        self.antenatal_visits_membership = mommy.make_recipe('td_maternal.antenatalenrollmenttwo', registered_subject=options.get('registered_subject'))

        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code='1010M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        mommy.make_recipe('td_maternal.maternallabdel', registered_subject=self.registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code='1020M')
        maternal_visit_1020M = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=maternal_visit_1020M.subject_identifier,
            reference_datetime=maternal_visit_1020M.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)

    def create_mother(self, status_options):
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **status_options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = mommy.make_recipe('td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000, number_of_gestations=1)
        self.antenatal_visits_membership = mommy.make_recipe('td_maternal.antenatalenrollmenttwo', registered_subject=status_options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code='1010M')
        self.antenatal_visit_1 = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

    def hiv_pos_mother_options(self, registered_subject):
        options = {'registered_subject': registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=25)).date()}
        return options

    def hiv_neg_mother_options(self, registered_subject):
        options = {'registered_subject': registered_subject,
                   'current_hiv_status': UNK,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (get_utcnow() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_result': NEG,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=34)).date()}
        return options
