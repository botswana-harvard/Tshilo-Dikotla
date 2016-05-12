from edc_constants.constants import SCREENED
from edc_registration.models import RegisteredSubject
from edc_constants.constants import FAILED_ELIGIBILITY, OFF_STUDY, SCHEDULED
from edc_meta_data.models import RequisitionMetaData
from tshilo_dikotla.apps.td_maternal.models import MaternalVisit, MaternalEligibility, MaternalEligibilityLoss

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory)


class TestMaternalUltrasound(BaseTestCase):
    """Test eligibility of a mother."""

    def setUp(self):
        super(TestMaternalUltrasound, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        # maternal visit created here.
        self.antenatal_enrollment = AntenatalEnrollmentFactory(registered_subject=self.registered_subject)

    def test_pass_eligibility_on_singleton_pregnancy(self):
        """Test antenatal Enrollment remains as eligible on singleton fetus ultrasound."""
        maternal_visit = MaternalVisit.objects.get(appointment__registered_subject=self.registered_subject,
                                                   reason=SCHEDULED,
                                                   appointment__visit_definition__code='1000M')
        self.assertEqual(MaternalVisit.objects.all().count(), 1)
        options = {'number_of_gestations': 1,
                   'maternal_visit': maternal_visit}
        maternal_ultrasound = MaternalUltraSoundIniFactory(**options)
        self.assertTrue(maternal_ultrasound.antenatal_enrollment.is_eligible)

    def test_fail_eligibility_on_non_singleton_pregnancy(self):
        """Test antenatal Enrollment fails eligible on non-singleton fetus ultrasound."""
        maternal_visit = MaternalVisit.objects.get(appointment__registered_subject=self.registered_subject,
                                                   reason=SCHEDULED,
                                                   appointment__visit_definition__code='1000M')
        options = {'number_of_gestations': 2,
                   'maternal_visit': maternal_visit}
        maternal_ultrasound = MaternalUltraSoundIniFactory(**options)
        self.assertFalse(maternal_ultrasound.antenatal_enrollment.is_eligible)

    def test_create_visit_with_offstudy_on_failure(self):
        """Offstudy visit created on antenatal enrollment failure."""
        maternal_visit = MaternalVisit.objects.get(appointment__registered_subject=self.registered_subject,
                                                   reason=SCHEDULED,
                                                   appointment__visit_definition__code='1000M')
        options = {'number_of_gestations': 2,
                   'maternal_visit': maternal_visit}
        maternal_ultrasound = MaternalUltraSoundIniFactory(**options)
        self.assertFalse(maternal_ultrasound.antenatal_enrollment.is_eligible)
        self.assertEqual(MaternalVisit.objects.filter(
            reason=FAILED_ELIGIBILITY,
            study_status=OFF_STUDY,
            appointment__registered_subject__subject_identifier=self.registered_subject.subject_identifier).count(), 1)

