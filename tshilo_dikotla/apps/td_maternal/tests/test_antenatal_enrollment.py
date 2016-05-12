from django.utils import timezone
from datetime import timedelta

from edc_constants.constants import POS, YES, NO, NEG, NOT_APPLICABLE, UNKNOWN, FAILED_ELIGIBILITY, OFF_STUDY

from .factories import (
    AntenatalEnrollmentFactory, MaternalEligibilityFactory, MaternalConsentFactory)


from ..models import MaternalVisit

from .base_test_case import BaseTestCase


class TestAntenatalEnrollment(BaseTestCase):
    """Test eligibility of a mother for antenatal enrollment."""

    def setUp(self):
        super(TestAntenatalEnrollment, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        self.data = {
            'registered_subject': self.registered_subject}

    def test_gestation_wks_below_16(self):
        """Test for a positive mother with evidence of hiv_status,
        on a valid regimen but weeks of gestation below 16."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=self.registered_subject,
            gestation_wks=15)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.off_study_visit_on_ineligible(antenatal_enrollment.subject_identifier)

    def test_gestation_wks_above_36(self):
        """Test for a positive mother with evidence of hiv_status,
        on a valid regimen but weeks of gestation above 36."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=self.registered_subject,
            gestation_wks=37)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.off_study_visit_on_ineligible(antenatal_enrollment.subject_identifier)

    def test_gestation_wks_between_16_and_36(self):
        """Test for a positive mother with evidence of hiv_status,
        on a valid regimen but weeks of gestation between 16 and 36."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=self.registered_subject,
            valid_regimen=YES,
            valid_regimen_duration=YES,
            gestation_wks=35)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_is_diabetic_ineligible(self):
        """Test for a positive mother with valid documentation,
        on a valid regimen but is diabetic."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=self.registered_subject,
            is_diabetic=YES)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.off_study_visit_on_ineligible(antenatal_enrollment.subject_identifier)

    def test_is_not_diabetic(self):
        """Test for a positive mother with valid documentation,
        on a valid regimen but not diabetic."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            is_diabetic=NO,
            valid_regimen=YES,
            valid_regimen_duration=YES,
            rapid_test_done=NOT_APPLICABLE)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_will_breastfeed(self):
        """Test for a negative mother with documentation evidence,
        amd who agrees to breastfeed for a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG,
            registered_subject=self.registered_subject,
            will_breastfeed=YES)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_will_not_breastfeed_ineligible(self):
        """Test for a negative mother who has documentation of hiv_status,
        but does not agree to breastfeed for a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG,
            registered_subject=self.registered_subject,
            will_breastfeed=NO)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.off_study_visit_on_ineligible(antenatal_enrollment.subject_identifier)

    def test_will_remain_onstudy(self):
        """Test for a negative mother who has documenation of hiv_status,
        and agrees to stay in study a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG,
            registered_subject=self.registered_subject,
            will_remain_onstudy=YES)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_not_will_remain_onstudy_ineligible(self):
        """Test for a negative mother who has documentatin of hiv_status,
        but does not agree to stay in study for a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG,
            registered_subject=self.registered_subject,
            will_remain_onstudy=NO
        )
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.off_study_visit_on_ineligible(antenatal_enrollment.subject_identifier)

    def test_positive_with_evidence(self):
        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NO,
            valid_regimen=YES,
            valid_regimen_duration=YES,
            registered_subject=self.registered_subject,)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_mother_tested_at_32weeks_with_evidence(self):
        """Test for a positive mother who tested at 32weeks,
        and has documentation of hiv_status with gestational age at 35weeks"""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=YES,
            week32_result=POS,
            rapid_test_date=timezone.now().date() - timedelta(weeks=5),
            evidence_hiv_status=YES,
            current_hiv_status=POS,
            registered_subject=self.registered_subject,
            rapid_test_done=NOT_APPLICABLE,
            valid_regimen=YES,
            valid_regimen_duration=YES,
            gestation_wks=35)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_mother_untested_at_32weeks_undergoes_rapid(self):
        """Test for a mother who is at 35weeks of gestational age,
        did not test at 32weeks, has no evidence of NEG hiv_status but undergoes rapid testing """

        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=NO,
            current_hiv_status=NEG,
            evidence_hiv_status=NO,
            rapid_test_done=YES,
            rapid_test_result=NEG,
            rapid_test_date=timezone.now().date(),
            registered_subject=self.registered_subject,
            gestation_wks=35)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_no_week32test_rapid_test_ineligible(self):
        """Test for a mother who is at 35weeks gestational age,
        did not test at week 32 and does a rapid test which is POS"""
        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=NO,
            week32_result=None,
            current_hiv_status=NEG,
            evidence_hiv_status=NO,
            rapid_test_done=YES,
            rapid_test_result=POS,
            rapid_test_date=timezone.now().date(),
            registered_subject=self.registered_subject,
            gestation_wks=35)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.off_study_visit_on_ineligible(antenatal_enrollment.subject_identifier)

    def test_no_week32test_does_rapid_test_too_late(self):
        """Test for a mother at 35weeks gestational age,
        who did not do hiv_testing at 32weeks but undergoes rapid testing"""
        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=NO,
            week32_result=None,
            rapid_test_done=YES,
            rapid_test_result=POS,
            rapid_test_date=timezone.now().date(),
            current_hiv_status=POS,
            evidence_hiv_status=NO,
            valid_regimen=NO,
            valid_regimen_duration=NO,
            registered_subject=self.registered_subject,
            gestation_wks=35)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_no_week32test_evidence_na(self):
        """Test for a mother who has eligible gestational weeks, who is
        not aware of current hiv_status but undergoes rapid testing """
        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=NO,
            week32_result='',
            evidence_hiv_status=NOT_APPLICABLE,
            valid_regimen=NOT_APPLICABLE,
            valid_regimen_duration=NOT_APPLICABLE,
            current_hiv_status=UNKNOWN,
            rapid_test_done=YES,
            rapid_test_result=NEG,
            registered_subject=self.registered_subject,
            gestation_wks=35)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_no_week32test_evidence_na_rapid_neg_ineligible(self):
        """Test for a mother who has eligible gestational weeks, who is
        not aware of current hiv_status but undergoes rapid testing """
        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=NO,
            week32_result='',
            evidence_hiv_status=NOT_APPLICABLE,
            valid_regimen=NOT_APPLICABLE,
            valid_regimen_duration=NOT_APPLICABLE,
            current_hiv_status=UNKNOWN,
            rapid_test_done=YES,
            rapid_test_result=POS,
            registered_subject=self.registered_subject,
            gestation_wks=35)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.off_study_visit_on_ineligible(antenatal_enrollment.subject_identifier)

    def off_study_visit_on_ineligible(self, subject_identifier):
        self.assertEqual(MaternalVisit.objects.filter(
            reason=FAILED_ELIGIBILITY,
            study_status=OFF_STUDY,
            appointment__registered_subject__subject_identifier=subject_identifier).count(), 1)
