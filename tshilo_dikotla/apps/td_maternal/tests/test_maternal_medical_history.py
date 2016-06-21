from dateutil.relativedelta import relativedelta
from django.utils import timezone

from edc_constants.constants import UNKNOWN, YES, NEG, NOT_APPLICABLE
from tshilo_dikotla.apps.td_maternal.models import MaternalVisit

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, AntenatalVisitMembershipFactory, MaternalRandomizationFactory,
                        MaternalVisitFactory)


class TestMaternalMedicalHistory(BaseTestCase):

    def setUp(self):
        super(TestMaternalMedicalHistory, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        maternal_options = {
            'registered_subject': self.registered_subject,
            'current_hiv_status': UNKNOWN,
            'evidence_hiv_status': None,
            'week32_test': YES,
            'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=4)).date(),
            'week32_result': NEG,
            'evidence_32wk_hiv_status': YES,
            'will_get_arvs': NOT_APPLICABLE,
            'rapid_test_done': YES,
            'rapid_test_result': NEG,
            'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**maternal_options)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=maternal_options.get('registered_subject'),
            reason='SCHEDULED',
            appointment__visit_definition__code='1000M')
