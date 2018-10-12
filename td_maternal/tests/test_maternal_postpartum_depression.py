from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from edc_constants.constants import UNKNOWN, YES, NEG, NOT_APPLICABLE, POS, NO
from edc_constants.constants import SCHEDULED, CONTINUOUS, STOPPED, RESTARTED

from td_maternal.forms import MaternalPostPartumDepForm
from td_maternal.models import MaternalPostPartumDep, MaternalVisit, Appointment

from .base_test_case import BaseTestCase
from .factories import MaternalEligibilityFactory, MaternalConsentFactory, MaternalLabourDelFactory
from .factories import AntenatalEnrollmentFactory, MaternalUltraSoundIniFactory, MaternalVisitFactory


class TestMaternalPostPartumDepression(BaseTestCase):

    def setUp(self):
        super(TestMaternalPostPartumDepression, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'knows_lmp': NO,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=20)).date()}
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,
            est_edd_ultrasound=timezone.now().date() + timedelta(days=120), ga_confrimation_method=1)

        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=options.get('registered_subject'),
                                                            live_infants_to_register=1)

        appointment = Appointment.objects.get(
            registered_subject=options.get('registered_subject'),
            visit_definition__code='2000M')
        MaternalVisitFactory(
            appointment=appointment)

        appointment = Appointment.objects.get(
            registered_subject=options.get('registered_subject'),
            visit_definition__code='2010M')
        self.maternal_visit = MaternalVisitFactory(
            appointment=appointment)

    def test_1(self):
        maternal_dep = MaternalPostPartumDep.objects.create(
            maternal_visit=self.maternal_visit,
            report_datetime=timezone.datetime.now(),
            laugh='Definitely not so much now',
            enjoyment='Rather less than I used to',
            blame='Yes, some of the time',
            anxious='No, not at all',
            panick='Yes, quite a lot',
            top='Yes, most of the time I haven\'t been able to cope at all',
            unhappy='Not very often',
            sad='Yes, most of the time',
            crying='Yes, most of the time',
            self_harm='Yes, quite often')
        self.assertEqual(maternal_dep.total_score, 21)

    def test_2(self):
        maternal_dep = MaternalPostPartumDep.objects.create(
            maternal_visit=self.maternal_visit,
            report_datetime=timezone.datetime.now(),
            laugh='Not at all',
            enjoyment='Hardly at all',
            blame='Yes, most of the time',
            anxious='Yes, very often',
            panick='Yes, quite a lot',
            top='Yes, most of the time I haven\'t been able to cope at all',
            unhappy='Yes, most of the time',
            sad='Yes, most of the time',
            crying='Yes, most of the time',
            self_harm='Yes, quite often')
        self.assertEqual(maternal_dep.total_score, 30)

    def test_3(self):
        maternal_dep = MaternalPostPartumDep.objects.create(
            maternal_visit=self.maternal_visit,
            report_datetime=timezone.datetime.now(),
            laugh='As much as I always could',
            enjoyment='As much as I ever did',
            blame='No, never',
            anxious='No, not at all',
            panick='No, not at all',
            top='No, I have been coping as well as ever',
            unhappy='No, never',
            sad='No, never',
            crying='No, never',
            self_harm='Never')
        self.assertEqual(maternal_dep.total_score, 0)

    def test_4(self):
        maternal_dep = MaternalPostPartumDep.objects.create(
            maternal_visit=self.maternal_visit,
            report_datetime=timezone.datetime.now(),
            laugh='As much as I always could',
            enjoyment='As much as I ever did',
            blame='No, never',
            anxious='Yes, sometimes',
            panick='No, not at all',
            top='No, most of the time I have coped quite well',
            unhappy='No, never',
            sad='No, never',
            crying='No, never',
            self_harm='Never')
        self.assertNotEqual(maternal_dep.total_score, 30)
