from dateutil.relativedelta import relativedelta
from django.utils import timezone
from edc_constants.constants import SCHEDULED, POS, YES, NO, NEG, NOT_APPLICABLE, UNK, IND
from edc_meta_data.models import RequisitionMetaData
from edc_appointment.models import Appointment
from edc_registration.models import RegisteredSubject

from td_maternal.models import MaternalVisit
from td_maternal.classes import MaternalStatusHelper
from td_infant.tests.factories import InfantVisitFactory, InfantBirthFactory

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, AntenatalVisitMembershipFactory, MaternalVisitFactory,
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
        randomization = MaternalRandomizationFactory(maternal_visit=self.antenatal_visit_1)
        MaternalLabourDelFactory(registered_subject=self.registered_subject)
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=randomization.maternal_visit.appointment.registered_subject,
                visit_definition__code='1020M'))
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=randomization.maternal_visit.appointment.registered_subject,
                visit_definition__code='2000M'))
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=randomization.maternal_visit.appointment.registered_subject,
                visit_definition__code='2010M'))
        maternal_visit_2020M = MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=randomization.maternal_visit.appointment.registered_subject,
                visit_definition__code='2020M'))
        status_helper = MaternalStatusHelper(maternal_visit_2020M)
        self.assertEqual(status_helper.hiv_status, POS)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW',
                                                            lab_entry__app_label='td_lab',
                                                            lab_entry__model_name='maternalrequisition',
                                                            lab_entry__requisition_panel__name='Viral Load',
                                                            appointment=self.antenatal_visit_1.appointment).count(), 1)

    def test_dnapcr_for_heu_infant(self):
        """test that for an HEU infant, then the DNA PCR requisition is made available."""
        self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
        randomization = MaternalRandomizationFactory(maternal_visit=self.antenatal_visit_1)
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=randomization.maternal_visit.appointment.registered_subject,
                visit_definition__code='1020M'))
        labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject)
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=labour_del.registered_subject.subject_identifier)
        InfantBirthFactory(maternal_labour_del=labour_del, registered_subject=infant_registered_subject)
        InfantVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=infant_registered_subject,
                visit_definition__code='2000'))
        InfantVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=infant_registered_subject,
                visit_definition__code='2010'))
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW',
                                                            lab_entry__app_label='td_lab',
                                                            lab_entry__model_name='infantrequisition',
                                                            lab_entry__requisition_panel__name='DNA PCR',
                                                            appointment__visit_definition__code='2010').count(), 1)

    def test_dnapcr_for_non_heu_infant(self):
        """test that for a NON HEU infant, then the DNA PCR requisition is NOT made available."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='1020M'))
        labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject)
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=labour_del.registered_subject.subject_identifier)
        InfantBirthFactory(maternal_labour_del=labour_del, registered_subject=infant_registered_subject)
        InfantVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=infant_registered_subject,
                visit_definition__code='2000'))
        InfantVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=infant_registered_subject,
                visit_definition__code='2010'))
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NOT_REQUIRED',
                                                            lab_entry__app_label='td_lab',
                                                            lab_entry__model_name='infantrequisition',
                                                            lab_entry__requisition_panel__name='DNA PCR',
                                                            appointment__visit_definition__code='2010').count(), 1)

    def test_ind_status_from_rapid_test(self):
        """test that we can figure out a posetive status taking in to consideration rapid tests."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='1020M'))
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2000M'))
        maternal_visit_2010M = MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2010M'))
        status_helper = MaternalStatusHelper(maternal_visit_2010M)
        self.assertEqual(status_helper.hiv_status, NEG)
        rapid_test = RapidTestResultFactory(maternal_visit=maternal_visit_2010M, result=IND)
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2020M'))
        maternal_visit_2060M = MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2060M'))
        status_helper = MaternalStatusHelper(maternal_visit_2060M)
        self.assertEqual(status_helper.hiv_status, IND)

    def test_neg_status_from_enrollment(self):
        """test that we can figure out a negative status with just the enrollment status."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        MaternalLabourDelFactory(registered_subject=self.registered_subject)
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='1020M'))
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2000M'))
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2010M'))
        maternal_visit_2020M = MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2020M'))
        status_helper = MaternalStatusHelper(maternal_visit_2020M)
        self.assertEqual(status_helper.hiv_status, NEG)

    def test_neg_status_from_rapid_test(self):
        """test that we can figure out a negative status taking in to consideration rapid tests."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='1020M'))
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2000M'))
        maternal_visit_2010M = MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2010M'))
        status_helper = MaternalStatusHelper(maternal_visit_2010M)
        self.assertEqual(status_helper.hiv_status, NEG)
        rapid_test = RapidTestResultFactory(maternal_visit=maternal_visit_2010M, result=NEG)
        # Visit within 3months of rapid test.
        maternal_visit_2020M = MaternalVisitFactory(
            report_datetime=rapid_test.result_date + relativedelta(months=1),
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2020M'))
        status_helper = MaternalStatusHelper(maternal_visit_2020M)
        self.assertEqual(status_helper.hiv_status, NEG)

    def test_unkown_status(self):
        """test that a negative result that is more than 3months old will lead to UNK status."""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='1020M'))
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2000M'))
        maternal_visit_2010M = MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2010M'))
        status_helper = MaternalStatusHelper(maternal_visit_2010M)
        self.assertEqual(status_helper.hiv_status, NEG)
        rapid_test = RapidTestResultFactory(maternal_visit=maternal_visit_2010M, result=NEG)
        # Visit within 3months of rapid test.
        maternal_visit_2020M = MaternalVisitFactory(
            report_datetime=rapid_test.result_date + relativedelta(months=4),
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2020M'))
        status_helper = MaternalStatusHelper(maternal_visit_2020M)
        self.assertEqual(status_helper.hiv_status, UNK)

    def test_eligible_for_cd4(self):
        pass

    def test_return_previous_visit_ordering(self):
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='1020M'))
        MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2000M'))
        maternal_visit_2010M = MaternalVisitFactory(
            appointment=Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code='2010M'))
        status_helper = MaternalStatusHelper(maternal_visit_2010M)
        self.assertEqual(len(status_helper.previous_visits), 5)
        self.assertEqual(status_helper.previous_visits[0].appointment.visit_definition.code, '2010M')
        self.assertEqual(status_helper.previous_visits[4].appointment.visit_definition.code, '1000M')

    def create_mother(self, status_options):
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**status_options)
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__registered_subject=status_options.get('registered_subject'),
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(maternal_visit=self.maternal_visit_1000,
                                                                number_of_gestations=1,
                                                                )
        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=status_options.get('registered_subject'))
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=status_options.get('registered_subject'),
                                                visit_definition__code='1010M'))

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
