from dateutil.relativedelta import relativedelta

from django.test import TestCase
from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_constants.constants import (
    POS, YES, NO, NEG, NOT_APPLICABLE, UNKNOWN)

from td.hiv_result import EnrollmentResultError


class TestAntenatalEnrollment(TestCase):
    """Test eligibility of a mother for antenatal enrollment."""

    def setUp(self):
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent',
            maternal_eligibility_reference=maternal_eligibility.reference_pk)
        self.subject_identifier = self.maternal_consent.subject_identifier

    def test_gestation_wks_lmp_below_16(self):
        """Test ineligible when weeks of gestation below 16."""
        options = {'subject_identifier': self.subject_identifier,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=10)).date()}
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **options)
        self.assertEqual(antenatal_enrollment.ga_lmp_enrollment_wks, 10)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_gestation_wks_lmp_above_36(self):
        """Test ineligible when weeks of gestation below 36"""
        options = dict(
            subject_identifier=self.subject_identifier,
            last_period_date=(get_utcnow() - relativedelta(weeks=37)).date())
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **options)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_gestation_wks_lmp_between_16_and_36_notvalid_arv(self):
        """Test ineligible with valid GA but not willing to get arv's."""

        options = {'subject_identifier': self.subject_identifier, 'will_get_arvs': NO}

        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **options)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_gestation_wks_lmp_between_16_and_36_valid_arv(self):
        """Test eligible for a positive mother with evidence of hiv_status,
        will go on a valid regimen and weeks of gestation between 16 and 36."""

        options = {'subject_identifier': self.subject_identifier,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES}
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **options)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_is_diabetic_ineligible(self):
        """Test ineligible for diabetic."""

        options = {'subject_identifier': self.subject_identifier, 'is_diabetic': YES}
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **options)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_is_not_diabetic(self):
        """Test eligible for non-diabetic."""
        options = {'subject_identifier': self.subject_identifier}
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **options)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_will_breastfeed(self):
        """Test eligible if willing to breastfeed for a year."""
        options = {'subject_identifier': self.subject_identifier,
                   'will_breastfeed': YES}
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **options)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_will_not_breastfeed_ineligible(self):
        """Test eligible if NOT willing to breastfeed for a year."""
        options = {'subject_identifier': self.subject_identifier, 'will_breastfeed': NO}
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **options)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_will_remain_onstudy(self):
        """Test willing to remain onstudy for the first 3years of baby's life."""
        options = {'subject_identifier': self.subject_identifier,
                   'will_remain_onstudy': YES}
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **options)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_not_will_remain_onstudy_ineligible(self):
        """Test NOT willing to remain onstudy for the first 3years of baby's life."""
        options = {'subject_identifier': self.subject_identifier,
                   'will_remain_onstudy': NO}
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **options)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_mother_tested_POS_at_32weeks_with_evidence(self):
        """Test eligible for a mother who tested POS at or after 32weeks and has documentation of hiv_status"""
        options = {'subject_identifier': self.subject_identifier,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (get_utcnow() + relativedelta(weeks=5)).date(),
                   'week32_result': POS,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': YES,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=34)).date()}
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **options)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_mother_tested_POS_32weeks_with_NO_evidence(self):
        """Test for a mother who tested POS at or after 32weeks and has NO documentation of hiv_status"""
        options = {'subject_identifier': self.subject_identifier,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (get_utcnow() - relativedelta(weeks=1)).date(),
                   'week32_result': POS,
                   'evidence_32wk_hiv_status': NO,
                   'will_get_arvs': YES,
                   'rapid_test_done': YES,
                   'rapid_test_result': POS,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=34)).date()}
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **options)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_mother_tested_POS_before_32weeks_rapidtest_not_enforced(self):
        """Test for a mother who tested POS BEFORE 32weeks, with documentation then rapid test not enforced"""
        options = {'subject_identifier': self.subject_identifier,
                   'report_datetime': get_utcnow(),
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (get_utcnow() - relativedelta(weeks=4)).date(),
                   'week32_result': POS,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'rapid_test_date': None,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=34)).date()}
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_mother_tested_NEG_after_32weeks_then_rapidtest_notenforced(self):
        """Test for a mother who tested NEG AFTER 32weeks, with documentation then rapid test not enforced"""

        options = {'subject_identifier': self.subject_identifier,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (get_utcnow() + relativedelta(weeks=5)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': NOT_APPLICABLE,
                   'rapid_test_result': None,
                   'rapid_test_date': None,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=34)).date()}
        with self.assertRaises(EnrollmentResultError):
            mommy.make_recipe('td_maternal.antenatalenrollment', **options)

    def test_mother_tested_NEG_no_LMP_rapidtest_enforced(self):
        """Test for a mother who tested NEG with documentation but no LMP then rapid test is enforced"""

        options = {'subject_identifier': self.subject_identifier,
                   'knows_lmp': NO,
                   'last_period_date': None,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (get_utcnow() + relativedelta(weeks=5)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': NOT_APPLICABLE,
                   'rapid_test_result': None,
                   'rapid_test_date': None,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=34)).date()}
        with self.assertRaises(EnrollmentResultError):
            mommy.make_recipe('td_maternal.antenatalenrollment', **options)

    def test_mother_untested_at_32weeks_undergoes_rapid(self):
        """Test for a mother who is at 35weeks of gestational age,
        did not test at 32weeks, has no evidence of NEG hiv_status but undergoes rapid testing """

        options = {'subject_identifier': self.subject_identifier,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'will_get_arvs': NOT_APPLICABLE,
                   'week32_test': NO,
                   'rapid_test_done': YES,
                   'rapid_test_date': get_utcnow().date(),
                   'rapid_test_result': NEG,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=35)).date()}

        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_lmp_not_provided_status(self):
        """Test enrollment status is PENDING if lmp is not provided."""
        options = {'subject_identifier': self.subject_identifier,
                   'knows_lmp': NO,
                   'last_period_date': None,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': NO,
                   'rapid_test_done': YES,
                   'rapid_test_date': get_utcnow().date(),
                   'rapid_test_result': POS}
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.assertTrue(antenatal_enrollment.pending_ultrasound)

    def test_no_calculations_if_no_lmp(self):
        """Test if no lmp then ga_by_lmp and edd_by_lmp are not calculated."""
        options = {'subject_identifier': self.subject_identifier,
                   'knows_lmp': NO,
                   'last_period_date': None,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': NO,
                   'rapid_test_done': YES,
                   'rapid_test_date': get_utcnow().date(),
                   'rapid_test_result': POS}
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.assertTrue(antenatal_enrollment.pending_ultrasound)
        self.assertIsNone(antenatal_enrollment.last_period_date)
        self.assertIsNone(antenatal_enrollment.ga_lmp_enrollment_wks)
        self.assertIsNone(antenatal_enrollment.edd_by_lmp)
        self.assertIsNone(antenatal_enrollment.date_at_32wks)
