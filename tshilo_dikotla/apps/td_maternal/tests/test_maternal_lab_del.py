from django.utils import timezone
from dateutil.relativedelta import relativedelta
from edc_constants.constants import SCREENED
from edc_registration.models import RegisteredSubject
from edc_identifier.models import SubjectIdentifier
from edc_constants.constants import FAILED_ELIGIBILITY, OFF_STUDY, SCHEDULED, POS, YES, NO, NEG, NOT_APPLICABLE
from edc_meta_data.models import RequisitionMetaData

from tshilo_dikotla.apps.td_maternal.models import MaternalVisit
from tshilo_dikotla.apps.td.constants import INFANT

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, AntenatalVisitMembershipFactory, MaternalLabourDelFactory)


class TestMaternalLabourDel(BaseTestCase):

    def setUp(self):
        super(TestMaternalLabourDel, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        # maternal visit created here.
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(maternal_visit=self.maternal_visit,
                                                                number_of_gestations=1,
                                                                )
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)

    def test_new_infant_registration(self):
        maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                       live_infants_to_register=1)
        self.assertEqual(SubjectIdentifier.objects.filter(
            identifier=self.registered_subject.subject_identifier).count(), 1)
        self.assertEqual(RegisteredSubject.objects.filter(
            subject_type=INFANT,
            registration_status='DELIVERED',
            relative_identifier=self.maternal_consent.subject_identifier).count(), 1)

    def test_on_therapy_for_atleast4weeks(self):
        self.assertEqual(self.antenatal_enrollment.enrollment_hiv_status, POS)
        maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                       live_infants_to_register=1,
                                                       valid_regiment_duration=YES
                                                       )
        self.assertTrue(maternal_labour_del.keep_on_study)
        self.assertTrue(maternal_labour_del.antenatal_enrollment.is_eligible)

    def test_not_therapy_for_atleast4weeks(self):
        self.assertEqual(self.antenatal_enrollment.enrollment_hiv_status, POS)
        maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                       live_infants_to_register=1,
                                                       valid_regiment_duration=NO
                                                       )
        self.assertFalse(maternal_labour_del.keep_on_study)
        self.assertFalse(maternal_labour_del.antenatal_enrollment.is_eligible)