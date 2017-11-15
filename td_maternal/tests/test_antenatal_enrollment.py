from edc_appointment.models import Appointment
from edc_constants.constants import (POS, YES, NO, NEG, NOT_APPLICABLE, UNKNOWN,
                                     FAILED_ELIGIBILITY, OFF_STUDY, ON_STUDY, SCHEDULED)

from dateutil.relativedelta import relativedelta
from django.utils import timezone

from ..forms import AntenatalEnrollmentForm
from ..models import MaternalVisit, EnrollmentHelper, MaternalOffStudy
from .base_test_case import BaseTestCase
from .factories import (
    AntenatalEnrollmentFactory, MaternalEligibilityFactory, MaternalConsentFactory)


class TestAntenatalEnrollment(BaseTestCase):
    """Test eligibility of a mother for antenatal enrollment."""

    def setUp(self):
        super(TestAntenatalEnrollment, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.registered_subject = self.maternal_eligibility.registered_subject
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
        self.data = {
            'registered_subject': self.registered_subject}

    def test_gestation_wks_lmp_below_16(self):
        """Test for a positive mother with evidence of hiv_status,
        will go on a valid regimen but weeks of gestation below 16."""
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=14)).date()}
        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        self.off_study_visit_on_ineligible(
            antenatal_enrollment.subject_identifier)

    def test_gestation_wks_lmp_above_36(self):
        """Test for a positive mother with evidence of hiv_status,
        will go on a valid regimen but weeks of gestation above 36."""

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=37)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        self.off_study_visit_on_ineligible(
            antenatal_enrollment.subject_identifier)

    def test_gestation_wks_lmp_between_16_and_36_notvalid_arv(self):
        """Test for a positive mother with evidence of hiv_status,
        will NOT go on a valid regimen and weeks of gestation between 16 and 36."""

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': NO,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        self.off_study_visit_on_ineligible(
            antenatal_enrollment.subject_identifier)

    def test_gestation_wks_lmp_between_16_and_36_valid_arv(self):
        """Test for a positive mother with evidence of hiv_status,
        will go on a valid regimen and weeks of gestation between 16 and 36."""

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(antenatal_enrollment.is_eligible)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        self.assertEqual(Appointment.objects.all().count(), 1)

    def test_is_diabetic_ineligible(self):
        """Test for a positive mother with valid documentation,
        will go on a valid regimen but is diabetic."""

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        self.off_study_visit_on_ineligible(
            antenatal_enrollment.subject_identifier)

    def test_is_not_diabetic(self):
        """Test for a positive mother with valid documentation,
        will go on a valid regimen but not diabetic."""

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(antenatal_enrollment.is_eligible)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        self.assertEqual(Appointment.objects.all().count(), 1)

    def test_will_breastfeed(self):
        """Test for a posetive mother with documentation evidence,
        and who agrees to breastfeed for a year."""
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_breastfeed': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(antenatal_enrollment.is_eligible)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        self.assertEqual(Appointment.objects.all().count(), 1)

    def test_will_not_breastfeed_ineligible(self):
        """Test for a posetive mother who has documentation of hiv_status,
        but does NOT agree to breastfeed for a year."""

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_breastfeed': NO,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        self.off_study_visit_on_ineligible(
            antenatal_enrollment.subject_identifier)

    def test_will_remain_onstudy(self):
        """Test for a posetive mother who has documenation of hiv_status,
        and agrees to stay in study a year."""

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(antenatal_enrollment.is_eligible)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        self.assertEqual(Appointment.objects.all().count(), 1)

    def test_not_will_remain_onstudy_ineligible(self):
        """Test for a posetive mother who has documentatin of hiv_status,
        but does not agree to stay in study for a year."""

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': NO,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        self.off_study_visit_on_ineligible(
            antenatal_enrollment.subject_identifier)

    def test_mother_tested_POS_at_32weeks_with_evidence(self):
        """Test for a mother who tested POS at or after 32weeks and has documentation of hiv_status"""

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() + relativedelta(weeks=5)).date(),
                   'week32_result': POS,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'rapid_test_date': None,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(antenatal_enrollment.is_eligible)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        self.assertEqual(Appointment.objects.all().count(), 1)

    def test_mother_tested_POS_32weeks_with_NO_evidence(self):
        """Test for a mother who tested POS at or after 32weeks and has NO documentation of hiv_status"""

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=1)).date(),
                   'week32_result': POS,
                   'evidence_32wk_hiv_status': NO,
                   'will_get_arvs': YES,
                   'rapid_test_done': YES,
                   'rapid_test_result': POS,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(antenatal_enrollment.is_eligible)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        self.assertEqual(Appointment.objects.all().count(), 1)

    def test_mother_tested_POS_before_32weeks_rapidtest_not_enforced(self):
        """Test for a mother who tested POS BEFORE 32weeks, with documentation then rapid test not enforced"""

        options = {'registered_subject': self.registered_subject,
                   'report_datetime': timezone.now(),
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=4)).date(),
                   'week32_result': POS,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'rapid_test_date': None,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        enrollment_helper = EnrollmentHelper(antenatal_enrollment)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        self.assertTrue(enrollment_helper.validate_rapid_test)

    def test_mother_tested_NEG_before_32weeks_then_rapidtest_enforced(self):
        """Test for a mother who tested NEG BEFORE 32weeks, then rapid test enforced,
        regardless of having documentation or not"""

        options = {'registered_subject': self.registered_subject,
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

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        enrollment_helper = EnrollmentHelper(antenatal_enrollment)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, NEG)
        self.assertFalse(enrollment_helper.validate_rapid_test)

    def test_mother_tested_NEG_after_32weeks_then_rapidtest_notenforced(self):
        """Test for a mother who tested NEG AFTER 32weeks, with documentation then rapid test not enforced"""

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() + relativedelta(weeks=5)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': NOT_APPLICABLE,
                   'rapid_test_result': None,
                   'rapid_test_date': None,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        enrollment_helper = EnrollmentHelper(antenatal_enrollment)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, NEG)
        self.assertTrue(enrollment_helper.validate_rapid_test)

#     def test_mother_tested_NEG_after_32weeks_then_rapidtest_notenforced(self):
#         """Test for a mother who tested NEG AFTER 32weeks, with documentation then rapid test not enforced"""
#
#         options = {'registered_subject': self.registered_subject,
#                    'current_hiv_status': UNKNOWN,
#                    'evidence_hiv_status': None,
#                    'week32_test': YES,
#                    'week32_test_date': (timezone.datetime.now() + relativedelta(weeks=5)).date(),
#                    'week32_result': NEG,
#                    'evidence_32wk_hiv_status': YES,
#                    'will_get_arvs': NOT_APPLICABLE,
#                    'rapid_test_done': NOT_APPLICABLE,
#                    'rapid_test_result': None,
#                    'rapid_test_date': None,
#                    'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}
#
#         antenatal_enrollment = AntenatalEnrollmentFactory(**options)
#         enrollment_helper = EnrollmentHelper(antenatal_enrollment)
#         self.assertEqual(antenatal_enrollment.enrollment_hiv_status, NEG)
#         self.assertTrue(enrollment_helper.validate_rapid_test)

    def test_mother_tested_NEG_no_LMP_rapidtest_enforced(self):
        """Test for a mother who tested NEG with documentation but no LMP then rapid test is enforced"""

        options = {'registered_subject': self.registered_subject,
                   'knows_lmp': NO,
                   'last_period_date': None,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() + relativedelta(weeks=5)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': NOT_APPLICABLE,
                   'rapid_test_result': None,
                   'rapid_test_date': None,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        enrollment_helper = EnrollmentHelper(antenatal_enrollment)
        self.assertTrue(enrollment_helper.validate_rapid_test)

    def test_mother_tested_NEG_after_32weeks_then_rapidtest_enforced_nodoc(self):
        """Test for a mother who tested NEG AFTER 32weeks, without documentation then rapid test is enforced"""

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=1)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': NO,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        enrollment_helper = EnrollmentHelper(antenatal_enrollment)
        self.assertFalse(enrollment_helper.validate_rapid_test)

    def test_mother_untested_at_32weeks_undergoes_rapid(self):
        """Test for a mother who is at 35weeks of gestational age,
        did not test at 32weeks, has no evidence of NEG hiv_status but undergoes rapid testing """

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': NO,
                   'rapid_test_done': YES,
                   'rapid_test_date': timezone.datetime.now().date(),
                   'rapid_test_result': NEG,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=35)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(antenatal_enrollment.is_eligible)
        self.scheduled_visit_on_eligible_or_pending(
            self.registered_subject.subject_identifier)

    def test_no_week32test_rapid_test_ineligible(self):
        """Test for a mother who is at 35weeks gestational age,
        did not test at week 32 and does a rapid test which is POS"""

        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': NO,
                   'rapid_test_done': YES,
                   'rapid_test_date': timezone.datetime.now().date(),
                   'rapid_test_result': POS,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=35)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.off_study_visit_on_ineligible(
            antenatal_enrollment.subject_identifier)

    def test_lmp_not_provided_status(self):
        """Test enrollment status is PENDING if lmp is not provided."""
        options = {'registered_subject': self.registered_subject,
                   'knows_lmp': NO,
                   'last_period_date': None,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': NO,
                   'rapid_test_done': YES,
                   'rapid_test_date': timezone.datetime.now().date(),
                   'rapid_test_result': POS}
        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.assertTrue(antenatal_enrollment.pending_ultrasound)
        self.scheduled_visit_on_eligible_or_pending(
            self.registered_subject.subject_identifier)

    def test_no_calculations_if_no_lmp(self):
        """Test if no lmp then ga_by_lmp and edd_by_lmp are not calculated."""
        options = {'registered_subject': self.registered_subject,
                   'knows_lmp': NO,
                   'last_period_date': None,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': NO,
                   'rapid_test_done': YES,
                   'rapid_test_date': timezone.datetime.now().date(),
                   'rapid_test_result': POS}
        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(antenatal_enrollment.pending_ultrasound)
        self.assertIsNone(antenatal_enrollment.last_period_date)
        self.assertIsNone(antenatal_enrollment.ga_lmp_enrollment_wks)
        self.assertIsNone(antenatal_enrollment.edd_by_lmp)
        self.assertIsNone(antenatal_enrollment.date_at_32wks)
        self.scheduled_visit_on_eligible_or_pending(
            self.registered_subject.subject_identifier)

#     def test_lt_16_weeks_lmp(self):
#
#         options = {'registered_subject': self.registered_subject,
#                    'report_datetime': timezone.datetime.now(),
#                    'current_hiv_status': UNKNOWN,
#                    'evidence_hiv_status': None,
#                    'week32_test': NO,
#                    'rapid_test_done': YES,
#                    'rapid_test_date': timezone.datetime.now().date(),
#                    'rapid_test_result': POS,
#                    'last_period_date': (timezone.datetime.now() - relativedelta(weeks=10)).date()}
#         form = AntenatalEnrollmentForm(data=options)
#         errors = ''.join(form.errors.get('__all__'))
#         self.assertIn(
#             'LMP cannot be within 16weeks of report datetime. '
#             'Got LMP as 2017-06-21 and report datetime as ', errors)

    def off_study_visit_on_ineligible(self, subject_identifier):
        self.assertEqual(MaternalVisit.objects.all().count(), 1)
        self.assertEqual(MaternalVisit.objects.filter(
            reason=FAILED_ELIGIBILITY,
            study_status=OFF_STUDY,
            appointment__registered_subject__subject_identifier=subject_identifier).count(), 1)

    def scheduled_visit_on_eligible_or_pending(self, subject_identifier):
        self.assertEqual(MaternalVisit.objects.all().count(), 1)
        self.assertEqual(MaternalOffStudy.objects.all().count(), 0)
        self.assertEqual(MaternalVisit.objects.filter(
            reason=SCHEDULED,
            study_status=ON_STUDY,
            appointment__registered_subject__subject_identifier=subject_identifier).count(), 1)
