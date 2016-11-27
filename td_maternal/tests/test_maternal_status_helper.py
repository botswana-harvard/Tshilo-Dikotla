from dateutil.relativedelta import relativedelta
from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NO, NEG, NOT_APPLICABLE, UNK, IND
from edc_registration.models import RegisteredSubject

from td.models import Appointment
from td_maternal.maternal_status_helper import MaternalStatusHelper
from td_maternal.models import RequisitionMetadata

from .base_test_case import BaseTestCase


class TestMaternalStatusHelper(BaseTestCase):

    def setUp(self):
        super(TestMaternalStatusHelper, self).setUp()
        self.maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_consent.registered_subject

    def test_pos_status_from_enrollment(self):
        """test that we can figure out a posetive status with just the enrollment status."""
        self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
        mommy.make_recipe('td_maternal.maternalrandomization', maternal_visit=self.antenatal_visit_1)
        mommy.make_recipe('td_maternal.maternalLabourdel', registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2020M')
        maternal_visit_2020M = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2020M)
        self.assertEqual(status_helper.hiv_status, POS)
        self.assertEqual(RequisitionMetadata.objects.filter(entry_status='REQUIRED',
                                                            model='td_lab.maternalrequisition',
                                                            panel_name='PBMC VL',
                                                            visit_code='2020M').count(), 1)

    def test_dnapcr_for_heu_infant(self):
        """test that for an HEU infant, then the DNA PCR requisition is made available."""
        self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
        mommy.make_recipe('td_maternal.maternalrandomization', maternal_visit=self.antenatal_visit_1)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        labour_del = mommy.make_recipe('td_maternal.maternalLabourdel', registered_subject=self.registered_subject)
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=labour_del.registered_subject.subject_identifier)
        mommy.make_recipe('td_infant.infantbirth', maternal_labour_del=labour_del, registered_subject=infant_registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.infant_registered_subject.subject_identifier, visit_code='2000')
        mommy.make_recipe('td_infant.infantvisit', appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.infant_registered_subject.subject_identifier, visit_code='2010')
        mommy.make_recipe('td_infant.infantvisit', appointment=self.appointment)
        self.assertEqual(RequisitionMetadata.objects.filter(entry_status='REQUIRED',
                                                            model='td_lab.infantrequisition',
                                                            panel_name='DNA PCR',
                                                            visit_code='2010').count(), 1)

    def test_dnapcr_for_non_heu_infant(self):
        """test that for a NON HEU infant, then the DNA PCR requisition is NOT made available."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        labour_del = mommy.make_recipe('td_maternal.maternallabourdel', registered_subject=self.registered_subject)
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=labour_del.registered_subject.subject_identifier)
        mommy.make_recipe('td_infant.infantbirth', maternal_labour_del=labour_del, registered_subject=infant_registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.infant_registered_subject.subject_identifier, visit_code='2000')
        mommy.make_recipe('td_infant.infantvisit', appointment=self.appointment)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.infant_registered_subject.subject_identifier, visit_code='2010')
        mommy.make_recipe('td_infant.infantvisit', appointment=self.appointment)
        self.assertEqual(RequisitionMetadata.objects.filter(entry_status='NOT_REQUIRED',
                                                            model='td_lab.infantrequisition',
                                                            panel_name='DNA PCR',
                                                            visit_code='2010').count(), 1)

    def test_ind_status_from_rapid_test(self):
        """test that we can figure out a posetive status taking in to consideration rapid tests."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        mommy.make_recipe('td_maternal.maternallabourdel', registered_subject=self.registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        maternal_visit_2010M = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2010M)
        self.assertEqual(status_helper.hiv_status, NEG)
        mommy.make_recipe('td_maternal.rapidtestresult', maternal_visit=maternal_visit_2010M, result=IND)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2020M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2060M')
        maternal_visit_2060M = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2060M)
        self.assertEqual(status_helper.hiv_status, IND)

    def test_neg_status_from_enrollment(self):
        """test that we can figure out a negative status with just the enrollment status."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        mommy.make_recipe('td_maternal.maternallabourdel', registered_subject=self.registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2020M')
        maternal_visit_2020M = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2020M)
        self.assertEqual(status_helper.hiv_status, NEG)

    def test_neg_status_from_rapid_test(self):
        """test that we can figure out a negative status taking in to consideration rapid tests."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        mommy.make_recipe('td_maternal.maternallabourdel', registered_subject=self.registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        maternal_visit_2010M = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2010M)
        self.assertEqual(status_helper.hiv_status, NEG)
        mommy.make_recipe('td_maternal.rapidtestresult', maternal_visit=maternal_visit_2010M, result=NEG)
        # Visit within 3months of rapid test.
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2020M')
        maternal_visit_2020M = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2020M)
        self.assertEqual(status_helper.hiv_status, NEG)

    def test_unkown_status(self):
        """test that a negative result that is more than 3months old will lead to UNK status."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        mommy.make_recipe('td_maternal.maternallabourdel', registered_subject=self.registered_subject)
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        maternal_visit_2010M = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2010M)
        self.assertEqual(status_helper.hiv_status, NEG)
        mommy.make_recipe(
            'td_maternal.rapidtestresult', maternal_visit=maternal_visit_2010M,
            result_date=(get_utcnow() - relativedelta(months=4)).date(),
            result=NEG)
        # Visit within 3months of rapid test.
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2020M')
        maternal_visit_2020M = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2020M)
        self.assertEqual(status_helper.hiv_status, UNK)

    def test_return_previous_visit_ordering(self):
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        mommy.make_recipe('td_maternal.maternallabourdel', registered_subject=self.registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        maternal_visit_2010M = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2010M)
        self.assertEqual(len(status_helper.previous_visits), 5)
        self.assertEqual(status_helper.previous_visits[0].appointment.visit_code, '1000M')
        self.assertEqual(status_helper.previous_visits[4].appointment.visit_code, '2010M')

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
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = mommy.make_recipe('td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000, number_of_gestations=1,)
        self.antenatal_visits_membership = mommy.make_recipe('td_maternal.antenatalenrollmenttwo', registered_subject=options.get('registered_subject'))

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1010M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        mommy.make_recipe('td_maternal.maternallabourdel', registered_subject=self.registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        maternal_visit_1020M = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_1020M)
        self.assertEqual(status_helper.hiv_status, NEG)

    def create_mother(self, status_options):
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **status_options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = mommy.make_recipe('td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000, number_of_gestations=1)
        self.antenatal_visits_membership = mommy.make_recipe('td_maternal.antenatalenrollmenttwo', registered_subject=status_options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1010M')
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
