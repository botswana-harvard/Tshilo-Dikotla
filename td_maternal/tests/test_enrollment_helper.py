from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NEG, NO

from td.hiv_status import EnrollmentStatusError

from ..enrollment_helper import EnrollmentHelper
from ..models import AntenatalEnrollment


class Obj:
    def __init__(self, **kwargs):
        for attr in [field.name for field in AntenatalEnrollment._meta.get_fields()]:
            setattr(self, attr, None)
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.report_datetime = get_utcnow()


class TestEnrollmentHelper(TestCase):

    def test_pos(self):
        """Asserts POS result with evidence is POS."""
        obj = Obj(current_hiv_status=POS, evidence_hiv_status=YES)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_hiv_status, POS)

    def test_result_pos_no_evidence(self):
        """Asserts POS result without evidence requires rapid."""
        obj = Obj(current_hiv_status=POS, evidence_hiv_status=NO)
        self.assertRaises(EnrollmentStatusError, EnrollmentHelper, obj)

    def test_result_neg_no_evidence(self):
        """Asserts NEG result with or without evidence is None."""
        obj = Obj(current_hiv_status=NEG, evidence_hiv_status=NO)
        self.assertRaises(EnrollmentStatusError, EnrollmentHelper, obj)
        obj = Obj(current_hiv_status=NEG, evidence_hiv_status=YES)
        self.assertRaises(EnrollmentStatusError, EnrollmentHelper, obj)

    def test_result_neg_by_week32(self):
        """Asserts NEG result by week 32 test alone requires rapid."""
        obj = Obj(
            week32_test_date=get_utcnow(),
            week32_test=YES,
            week32_result=NEG,
            evidence_32wk_hiv_status=YES)
        self.assertRaises(EnrollmentStatusError, EnrollmentHelper, obj)

    def test_result_pos_by_week32_requires_rapid(self):
        """Asserts POS result by week 32 test."""
        obj = Obj(
            week32_test_date=get_utcnow(),
            week32_test=YES,
            week32_result=POS,
            evidence_32wk_hiv_status=YES)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_hiv_status, POS)

    def test_result_neg_by_week32_with_rapid(self):
        """Asserts NEG result by week 32 is NEG if supported by rapid."""
        obj = Obj(
            week32_test_date=get_utcnow(),
            week32_test=YES,
            week32_result=NEG,
            evidence_32wk_hiv_status=YES,
            rapid_test_date=get_utcnow(),
            rapid_test_done=YES,
            rapid_test_result=NEG)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_hiv_status, NEG)

    def test_result_neg_by_rapid(self):
        """Asserts NEG result by rapid test."""
        obj = Obj(
            current_hiv_status=NEG,
            evidence_hiv_status=NO,
            rapid_test_date=get_utcnow(),
            rapid_test_done=YES,
            rapid_test_result=NEG)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_hiv_status, NEG)

    def test_result_pos_by_rapid(self):
        """Asserts POS result by rapid test."""
        obj = Obj(
            current_hiv_status=NEG,
            evidence_hiv_status=NO,
            rapid_test_date=get_utcnow(),
            rapid_test_done=YES,
            rapid_test_result=POS)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_hiv_status, POS)
