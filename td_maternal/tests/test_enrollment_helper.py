import unittest

from dateutil.relativedelta import relativedelta

from django.test import TestCase, tag

from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NEG, NO, NOT_APPLICABLE
from edc_pregnancy_utils import Lmp

from ..enrollment_helper import EnrollmentHelper, Obj as ModellikeObj
from ..models import AntenatalEnrollment

from .test_mixins import MotherMixin


class Obj(ModellikeObj):
    def __init__(self, **kwargs):
        super(Obj, self).__init__(**kwargs)
        for attr in [field.name for field in AntenatalEnrollment._meta.get_fields()]:
            setattr(self, attr, None)
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.report_datetime = get_utcnow()


@tag('enrollment', 'pos', 'neg')
class TestResult(unittest.TestCase):

    def test_pos(self):
        """Asserts POS result with evidence is POS."""
        obj = Obj(current_hiv_status=POS, evidence_hiv_status=YES)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_result.result, POS)

    def test_result_pos_no_evidence(self):
        """Asserts POS result without evidence requires rapid."""
        obj = Obj(current_hiv_status=POS, evidence_hiv_status=NO)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertIn('rapid test is required for enrollment', enrollment_helper.messages.as_string())

    def test_result_neg_no_evidence(self):
        """Asserts NEG result with or without evidence is None."""
        obj = Obj(current_hiv_status=NEG, evidence_hiv_status=NO)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertIn('rapid test is required for enrollment', enrollment_helper.messages.as_string())
        self.assertIsNone(enrollment_helper.enrollment_result.result)
        obj = Obj(current_hiv_status=NEG, evidence_hiv_status=YES)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertIn('rapid test is required for enrollment', enrollment_helper.messages.as_string())
        self.assertIsNone(enrollment_helper.enrollment_result.result)

    @tag('investigate')
    # is this considered recent because it is a test on or after 32 weeks GA
    # or that it is a test done within 3 months?
    def test_result_neg_by_week32(self):
        """Asserts NEG result by week 32 test alone requires rapid if more than 3m old?."""
        obj = Obj(
            report_datetime=get_utcnow(),
            week32_test_date=get_utcnow().date(),
            week32_test=YES,
            week32_result=NEG,
            evidence_32wk_hiv_status=YES,
            will_get_arvs=NOT_APPLICABLE)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertFalse(enrollment_helper.messages)
        self.assertEqual(enrollment_helper.enrollment_result.result, NEG)
        obj = Obj(
            report_datetime=get_utcnow(),
            week32_test_date=(get_utcnow() - (relativedelta(months=4))).date(),
            week32_test=YES,
            week32_result=NEG,
            evidence_32wk_hiv_status=YES,
            will_get_arvs=NOT_APPLICABLE)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertIn('rapid test is required for enrollment', enrollment_helper.messages.as_string())
        self.assertIsNone(enrollment_helper.enrollment_result.result)

    def test_result_pos_by_week32_requires_rapid(self):
        """Asserts POS result by week 32 test."""
        obj = Obj(
            week32_test_date=get_utcnow(),
            week32_test=YES,
            week32_result=POS,
            evidence_32wk_hiv_status=YES,
            will_get_arvs=YES)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_result.result, POS)

    def test_result_neg_by_week32_with_rapid(self):
        """Asserts NEG result by week 32 is NEG if supported by rapid."""
        obj = Obj(
            week32_test_date=get_utcnow(),
            week32_test=YES,
            week32_result=NEG,
            evidence_32wk_hiv_status=YES,
            rapid_test_date=get_utcnow(),
            rapid_test_done=YES,
            rapid_test_result=NEG,
            will_get_arvs=NOT_APPLICABLE)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_result.result, NEG)

    def test_result_neg_by_rapid(self):
        """Asserts NEG result by rapid test."""
        obj = Obj(
            current_hiv_status=NEG,
            evidence_hiv_status=NO,
            rapid_test_date=get_utcnow(),
            rapid_test_done=YES,
            rapid_test_result=NEG,
            will_get_arvs=NOT_APPLICABLE)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_result.result, NEG)

    def test_result_pos_by_rapid(self):
        """Asserts POS result by rapid test."""
        obj = Obj(
            current_hiv_status=NEG,
            evidence_hiv_status=NO,
            rapid_test_date=get_utcnow(),
            rapid_test_done=YES,
            rapid_test_result=POS,
            will_get_arvs=YES)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_result.result, POS)


@tag('reviewed')
class TestGa(unittest.TestCase):

    opts = dict(
        current_hiv_status=POS,
        evidence_hiv_status=YES)

    def test_ga_by_lmp_out_of_range(self):
        """Asserts GA 15, not 16-36, ga_pending will be False."""
        obj = Obj(
            last_period_date=get_utcnow() - relativedelta(weeks=15),
            **self.opts)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.ga.weeks, 15)
        self.assertFalse(enrollment_helper.ga_pending)
        self.assertFalse(enrollment_helper.is_eligible)

    def test_ga_by_lmp_in_range_16(self):
        """Asserts GA 16, in 16-36."""
        obj = Obj(
            last_period_date=get_utcnow() - relativedelta(weeks=16),
            **self.opts)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.ga.weeks, 16)
        self.assertFalse(enrollment_helper.ga_pending)

    def test_ga_by_lmp_in_range_17(self):
        """Asserts GA 17, in 16-36."""
        obj = Obj(
            last_period_date=get_utcnow() - relativedelta(weeks=17),
            **self.opts)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.ga.weeks, 17)
        self.assertFalse(enrollment_helper.ga_pending)

    def test_ga_by_lmp_in_range_36(self):
        """Asserts GA 66, in 16-36."""
        obj = Obj(
            last_period_date=get_utcnow() - relativedelta(weeks=36),
            **self.opts)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.ga.weeks, 36)
        self.assertFalse(enrollment_helper.ga_pending)

    def test_ga_absurd(self):
        """Asserts GA none if absurd, ga_pending will be True"""
        obj = Obj(
            last_period_date=get_utcnow() - relativedelta(weeks=40),
            **self.opts)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.ga.weeks, 40)
        self.assertFalse(enrollment_helper.ga_pending)
        self.assertFalse(enrollment_helper.is_eligible)

    def test_ga_none(self):
        """Asserts GA none if lmp not know."""
        obj = Obj(
            last_period_date=None,
            **self.opts)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.ga.weeks, None)
        self.assertTrue(enrollment_helper.ga_pending)


@tag('reviewed')
class TestEdd(MotherMixin, TestCase):

    def test_edd_and_ga_is_from_lmp(self):
        """Asserts GA none if lmp not know."""
        self.make_positive_mother()
        lmp = self.get_utcnow() - relativedelta(weeks=25)
        lmp = Lmp(lmp=lmp, reference_date=self.antenatal_enrollment.report_datetime)
        self.assertIsNotNone(lmp.edd)
        self.assertEqual(self.antenatal_enrollment.edd_by_lmp, lmp.edd)
        self.assertEqual(self.antenatal_enrollment.ga_lmp_enrollment_wks, lmp.ga.weeks)
        self.assertEqual(self.antenatal_enrollment.ga_by_lmp, 25)
        self.assertFalse(self.antenatal_enrollment.ga_pending)
        self.assertTrue(self.antenatal_enrollment.is_eligible)

    def test_edd_ultrasound(self):
        """Asserts EDD from ultrasound is used."""
        lmp_27wks_ago = self.get_utcnow() - relativedelta(weeks=27)
        self.make_positive_mother(last_period_date=lmp_27wks_ago)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.add_maternal_visit('1000M')
        self.make_ultrasound()  # by default is 20 weeks
        # self.assertEqual(antenatal_enrollment.edd_by_lmp, datetime(2017, 2, 7))  # not by LMP!
        self.requery_antenatal_enrollment()
        self.assertEqual(self.antenatal_enrollment.enrollment_ga, 20)
        self.assertFalse(self.antenatal_enrollment.ga_pending)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
