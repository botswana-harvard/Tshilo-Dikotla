from dateutil.relativedelta import relativedelta
from django.utils import timezone
from model_mommy import mommy

from edc_call_manager.models import Call
from edc_constants.constants import POS, YES, NO, NEG, NOT_APPLICABLE, UNK

from td.models import Appointment

from .base_test_case import BaseTestCase


class TestPotentialCalls(BaseTestCase):

    def setUp(self):
        super(TestPotentialCalls, self).setUp()
        self.maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent = mommy.make_recipe('td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility)
        self.subject_identifier = self.maternal_consent.subject_identifier

    def test_appointment_creates_potential_call(self):
        """test that creating an appointment creates a similar potential call record"""
        self.create_mother(self.hiv_neg_mother_options(self.subject_identifier))
        self.assertTrue(Call.objects.filter(subject_identifier=self.registered_subject.subject_identifier).exists())
        # self.assertTrue(Call.objects.filter(subject_identifier=self.registered_subject.subject_identifier).exists())
        # MaternalLabDelFactory(registered_subject=self.registered_subject)
        # self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier).exists())
        # self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier).exists())
        # self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier).exists())
        # self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier).exists())
        # self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier).exists())
        # self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier).exists())
        # self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier).exists())
        # self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier).exists())
        # self.assertTrue(PotentialCall.objects.filter(subject_identifier=self.registered_subject.subject_identifier).exists())

    def create_mother(self, status_options):
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', subject_identifier=self.maternal_consent.subject_identifier)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000,
            subject_identifier=self.maternal_consent.subject_identifier)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalenrollmenttwo', subject_identifier=self.maternal_consent.subject_identifier)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1010M')
        self.antenatal_visit_1 = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

    def hiv_pos_mother_options(self, subject_identifier):
        options = {'subject_identifier': subject_identifier,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        return options

    def hiv_neg_mother_options(self, subject_identifier):
        options = {'subject_identifier': subject_identifier,
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
