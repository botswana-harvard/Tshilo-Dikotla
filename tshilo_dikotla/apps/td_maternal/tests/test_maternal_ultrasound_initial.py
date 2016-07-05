from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from edc_consent.models import ConsentType
from edc_registration.models import RegisteredSubject
from tshilo_dikotla.apps.td_maternal.models import MaternalVisit, MaternalUltraSoundInitial
from edc_constants.constants import SCHEDULED, YES, NO, UNKNOWN, NOT_APPLICABLE, NEG, POS

from .base_test_case import BaseTestCase
from .factories import MaternalEligibilityFactory, MaternalConsentFactory, AntenatalEnrollmentFactory, MaternalUltraSoundIniFactory

from tshilo_dikotla.apps.td_maternal.forms import MaternalUltraSoundInitialForm


class TestMaternalUltraSoundInitial(BaseTestCase):

    def setUp(self):
        super(TestMaternalUltraSoundInitial, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.assertEqual(self.maternal_consent.version, '1')
        self.registered_subject = self.maternal_consent.registered_subject
        self.assertEqual(ConsentType.objects.all().count(), 1)
        self.assertEqual(ConsentType.objects.all()[0].version, self.maternal_consent.version)
        self.assertEqual(self.registered_subject.subject_identifier, self.maternal_consent.subject_identifier)
        # maternal visit created here.
        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        options = {'number_of_gestations': 1,
                   'maternal_visit': self.maternal_visit,
                   'bpd': 200,
                   'hc': 200,
                   'ac': 200,
                   'fl': 200,
                   'ga_by_lmp': 100,
                   'ga_by_ultrasound_wks': 7,
                   'ga_by_ultrasound_days': 5,
                   'est_fetal_weight': 700,
                   'edd_confirmed': timezone.now() + timedelta(days=90),
                   'ga_confirmed': 7,
                   'est_edd': self.antenatal_enrollment.edd_by_lmp + relativedelta(days=17)}
        self.maternal_ultrasound_init = MaternalUltraSoundInitial.objects.create(**options)
        self.assertTrue(self.maternal_ultrasound_init.antenatal_enrollment.is_eligible)

    def test_maternal_ultra_init(self):
        self.assertEqual(MaternalUltraSoundInitial.objects.all().count(), 1)
