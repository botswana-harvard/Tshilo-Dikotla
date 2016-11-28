from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NEG, NO

from ..enrollment_helper import EnrollmentHelper, Week32, Current, EnrollmentStatusError
from ..models import AntenatalEnrollment
from dateutil.relativedelta import relativedelta


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


class TestRapid(TestCase):

    def test_rapid(self):
        pass


class TestCurrent(TestCase):

    def test_pos_with_evidence(self):
        """Assert POS from week32 class with evidence is POS."""
        obj = Obj(current_hiv_status=POS, evidence_hiv_status=YES)
        current = Current(obj)
        self.assertEqual(current.result, POS)

    def test_none_without_evidence(self):
        """Assert POS from week32 class with evidence is POS."""
        obj = Obj(current_hiv_status=POS, evidence_hiv_status=NO)
        current = Current(obj)
        self.assertEqual(current.result, None)
        obj = Obj(current_hiv_status=NEG, evidence_hiv_status=NO)
        current = Current(obj)
        self.assertEqual(current.result, None)

    def test_none_if_neg(self):
        """Assert POS from week32 class with evidence is POS."""
        obj = Obj(current_hiv_status=NEG, evidence_hiv_status=NO)
        current = Current(obj)
        self.assertEqual(current.result, None)
        obj = Obj(current_hiv_status=NEG, evidence_hiv_status=YES)
        current = Current(obj)
        self.assertEqual(current.result, None)


class TestWeek32(TestCase):

    def test_week32_result_pos(self):
        """Assert POS from week32 class with evidence is POS."""
        obj = Obj(
            week32_test=YES,
            week32_test_date=get_utcnow().date(),
            week32_result=POS,
            evidence_32wk_hiv_status=YES)
        week32 = Week32(obj)
        self.assertEqual(week32.result, POS)

    def test_week32_result_pos_without_evidence_is_none(self):
        """Assert POS from week32 class with evidence is POS."""
        obj = Obj(
            week32_test=YES,
            week32_test_date=get_utcnow().date(),
            week32_result=POS,
            evidence_32wk_hiv_status=NO)
        week32 = Week32(obj)
        self.assertEqual(week32.result, None)

    def test_week32_result_none_if_not_tested(self):
        """Assert None if no test."""
        obj = Obj(week32_test=NO)
        week32 = Week32(obj)
        self.assertEqual(week32.result, None)

    def test_week32_result_none_if_not_tested2(self):
        """Assert None if no test."""
        obj = Obj()
        week32 = Week32(obj)
        self.assertEqual(week32.result, None)

    def test_week32_result_neg_with_evidence(self):
        """Assert NEG from week32 class with evidence is NEG."""
        obj = Obj(
            week32_test=YES,
            week32_test_date=get_utcnow().date(),
            week32_result=NEG,
            evidence_32wk_hiv_status=YES)
        week32 = Week32(obj)
        self.assertEqual(week32.result, NEG)

    def test_week32_result_neg_without_evidence(self):
        """Assert NEG from week32 class without evidence is still NEG."""
        obj = Obj(
            week32_test=YES,
            week32_test_date=get_utcnow().date(),
            week32_result=NEG,
            evidence_32wk_hiv_status=NO)
        week32 = Week32(obj)
        self.assertEqual(week32.result, None)

    def test_week32_result_neg_4months(self):
        """Assert NEG from week32 class 4 months old is None."""
        obj = Obj(
            week32_test=YES,
            week32_test_date=(get_utcnow() - relativedelta(months=4)).date(),
            week32_result=NEG,
            evidence_32wk_hiv_status=NO)
        week32 = Week32(obj)
        self.assertEqual(week32.result, None)

    def test_week32_testdate_not_within3m(self):
        """Assert .within3m False if testdate 4m ago."""
        date_4m_ago = (get_utcnow() - relativedelta(months=4)).date()
        obj = Obj(
            week32_test=YES,
            week32_test_date=date_4m_ago,
            week32_result=POS,
            evidence_32wk_hiv_status=YES)
        week32 = Week32(obj)
        self.assertEqual(week32.within_3m, False)

    def test_week32_testdate_within3m_less_day(self):
        """Assert .within3m True if testdate 3m ago less one day."""
        date_3m_ago_less_day = (get_utcnow() - relativedelta(months=3) - relativedelta(days=1)).date()
        obj = Obj(
            week32_test=YES,
            week32_test_date=date_3m_ago_less_day,
            week32_result=POS,
            evidence_32wk_hiv_status=YES)
        week32 = Week32(obj)
        self.assertEqual(week32.within_3m, False)

    def test_week32_testdate_within3m_exact(self):
        """Assert .within3m False if testdate 3m ago (not inclusive)."""
        date_3m_ago = (get_utcnow() - relativedelta(months=3)).date()
        obj = Obj(
            week32_test=YES,
            week32_test_date=date_3m_ago,
            week32_result=POS,
            evidence_32wk_hiv_status=YES)
        week32 = Week32(obj)
        self.assertEqual(week32.within_3m, False)

    def test_week32_testdate_within3m_plus_day(self):
        """Assert .within3m False if testdate 3m ago + day."""
        date_3m_ago_plus_day = (get_utcnow() - relativedelta(months=3) + relativedelta(days=1)).date()
        obj = Obj(
            week32_test=YES,
            week32_test_date=date_3m_ago_plus_day,
            week32_result=POS,
            evidence_32wk_hiv_status=YES)
        week32 = Week32(obj)
        self.assertEqual(week32.within_3m, True)

    def test_week32_testdate_within3m_less_month(self):
        """Assert .within3m False if testdate 3m ago + day."""
        date_2m_ago = (get_utcnow() - relativedelta(months=2)).date()
        obj = Obj(
            week32_test=YES,
            week32_test_date=date_2m_ago,
            week32_result=POS,
            evidence_32wk_hiv_status=YES)
        week32 = Week32(obj)
        self.assertEqual(week32.within_3m, True)
