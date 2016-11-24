from dateutil.relativedelta import relativedelta
from django.utils import timezone
from edc_constants.constants import POS, YES, NO, NEG, NOT_APPLICABLE, UNK, IND
from td_maternal.models import RequisitionMetadata
from td_appointment.models import Appointment
from td_registration.models import RegisteredSubject

from td_maternal.classes import MaternalStatusHelper
from td_infant.tests.factories import InfantVisitFactory, InfantBirthFactory

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, AntenatalEnrollmentTwoFactory, MaternalVisitFactory,
                        MaternalRandomizationFactory, MaternalLabourDelFactory, RapidTestResultFactory)


class TestMaternalStatusHelper(BaseTestCase):

    def setUp(self):
        super(TestMaternalStatusHelper, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

    def test_pos_status_from_enrollment(self):
        """test that we can figure out a posetive status with just the enrollment status."""
        self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
        MaternalRandomizationFactory(maternal_visit=self.antenatal_visit_1)
        MaternalLabourDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2020M')
        maternal_visit_2020M = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2020M)
        self.assertEqual(status_helper.hiv_status, POS)
        self.assertEqual(RequisitionMetadata.objects.filter(entry_status='REQUIRED',
                                                            model='td_lab.maternalrequisition',
                                                            panel_name='PBMC VL',
                                                            visit_code='2020M').count(), 1)

    def test_dnapcr_for_heu_infant(self):
        """test that for an HEU infant, then the DNA PCR requisition is made available."""
        self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
        MaternalRandomizationFactory(maternal_visit=self.antenatal_visit_1)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject)
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=labour_del.registered_subject.subject_identifier)
        InfantBirthFactory(maternal_labour_del=labour_del, registered_subject=infant_registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.infant_registered_subject.subject_identifier, visit_code='2000')
        InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.infant_registered_subject.subject_identifier, visit_code='2010')
        InfantVisitFactory(
            appointment=self.appointment)
        self.assertEqual(RequisitionMetadata.objects.filter(entry_status='REQUIRED',
                                                            model='td_lab.infantrequisition',
                                                            panel_name='DNA PCR',
                                                            visit_code='2010').count(), 1)

    def test_dnapcr_for_non_heu_infant(self):
        """test that for a NON HEU infant, then the DNA PCR requisition is NOT made available."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject)
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=labour_del.registered_subject.subject_identifier)
        InfantBirthFactory(maternal_labour_del=labour_del, registered_subject=infant_registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.infant_registered_subject.subject_identifier, visit_code='2000')
        InfantVisitFactory(appointment=self.appointment)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.infant_registered_subject.subject_identifier, visit_code='2010')
        InfantVisitFactory(
            appointment=self.appointment)
        self.assertEqual(RequisitionMetadata.objects.filter(entry_status='NOT_REQUIRED',
                                                            model='td_lab.infantrequisition',
                                                            panel_name='DNA PCR',
                                                            visit_code='2010').count(), 1)

    def test_ind_status_from_rapid_test(self):
        """test that we can figure out a posetive status taking in to consideration rapid tests."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        maternal_visit_2010M = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2010M)
        self.assertEqual(status_helper.hiv_status, NEG)
        RapidTestResultFactory(maternal_visit=maternal_visit_2010M, result=IND)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2060M')
        maternal_visit_2060M = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2060M)
        self.assertEqual(status_helper.hiv_status, IND)

    def test_neg_status_from_enrollment(self):
        """test that we can figure out a negative status with just the enrollment status."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        MaternalLabourDelFactory(registered_subject=self.registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2020M')
        maternal_visit_2020M = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2020M)
        self.assertEqual(status_helper.hiv_status, NEG)

    def test_neg_status_from_rapid_test(self):
        """test that we can figure out a negative status taking in to consideration rapid tests."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        MaternalLabourDelFactory(registered_subject=self.registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        maternal_visit_2010M = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2010M)
        self.assertEqual(status_helper.hiv_status, NEG)
        RapidTestResultFactory(maternal_visit=maternal_visit_2010M, result=NEG)
        # Visit within 3months of rapid test.
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2020M')
        maternal_visit_2020M = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2020M)
        self.assertEqual(status_helper.hiv_status, NEG)

    def test_unkown_status(self):
        """test that a negative result that is more than 3months old will lead to UNK status."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalLabourDelFactory(registered_subject=self.registered_subject)
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        maternal_visit_2010M = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2010M)
        self.assertEqual(status_helper.hiv_status, NEG)
        RapidTestResultFactory(
            maternal_visit=maternal_visit_2010M,
            result_date=(timezone.now() - relativedelta(months=4)).date(),
            result=NEG)
        # Visit within 3months of rapid test.
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2020M')
        maternal_visit_2020M = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_2020M)
        self.assertEqual(status_helper.hiv_status, UNK)

    def test_return_previous_visit_ordering(self):
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        MaternalLabourDelFactory(registered_subject=self.registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        maternal_visit_2010M = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
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
                   'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': NO,
                   'rapid_test_date': None,
                   'rapid_test_result': None,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(maternal_visit=self.maternal_visit_1000,
                                                                number_of_gestations=1,)
        self.antenatal_visits_membership = AntenatalEnrollmentTwoFactory(
            registered_subject=options.get('registered_subject'))

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1010M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        MaternalLabourDelFactory(registered_subject=self.registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        maternal_visit_1020M = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        status_helper = MaternalStatusHelper(maternal_visit_1020M)
        self.assertEqual(status_helper.hiv_status, NEG)

    def create_mother(self, status_options):
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**status_options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(maternal_visit=self.maternal_visit_1000,
                                                                number_of_gestations=1,
                                                                )
        self.antenatal_visits_membership = AntenatalEnrollmentTwoFactory(
            registered_subject=status_options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1010M')
        self.antenatal_visit_1 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

    def hiv_pos_mother_options(self, registered_subject):
        options = {'registered_subject': registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        return options

    def hiv_neg_mother_options(self, registered_subject):
        options = {'registered_subject': registered_subject,
                   'current_hiv_status': UNK,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_result': NEG,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}
        return options
