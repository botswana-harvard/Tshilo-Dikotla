from dateutil.relativedelta import relativedelta
from django.utils import timezone
from edc_constants.constants import FAILED_ELIGIBILITY, OFF_STUDY, SCHEDULED, POS, YES, NO, NEG, NOT_APPLICABLE, UNK
from td_appointment.models import Appointment

from td_maternal.models import MaternalVisit, PotentialCall

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, AntenatalVisitMembershipFactory, MaternalVisitFactory,
                        MaternalLabourDelFactory)


class TestPotentialCalls(BaseTestCase):

    def setUp(self):
        super(TestPotentialCalls, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

    def test_appointment_creates_potential_call(self):
        """test that creating an appointment creates a similar potential call record"""
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier,
                                                     visit_code='1010M').exists())
        self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier,
                                                     visit_code='1020M').exists())
        MaternalLabourDelFactory(registered_subject=self.registered_subject)
        self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier,
                                                     visit_code='2000M').exists())
        self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier,
                                                     visit_code='2010M').exists())
        self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier,
                                                     visit_code='2020M').exists())
        self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier,
                                                     visit_code='2060M').exists())
        self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier,
                                                     visit_code='2120M').exists())
        self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier,
                                                     visit_code='2180M').exists())
        self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier,
                                                     visit_code='2240M').exists())
        self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier,
                                                     visit_code='2300M').exists())
        self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier,
                                                     visit_code='2360M').exists())

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