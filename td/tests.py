from faker import Faker
from django.test import TestCase

from edc_base.faker import EdcBaseProvider
from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NEG, NO, UNK, IND

from dateutil.relativedelta import relativedelta

from .hiv_result import Recent, Current, Rapid, EnrollmentResult, PostEnrollmentResult, Test, ElisaRequiredError
from td.hiv_result import RapidTestRequiredError

fake = Faker()
fake.add_provider(EdcBaseProvider)


class Obj:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.report_datetime = get_utcnow()


class TestRapid(TestCase):

    def test_rapid_pos(self):
        dt = get_utcnow()
        rapid = Rapid(reference_datetime=get_utcnow(), result=POS, result_date=dt)
        self.assertEqual(rapid.result, POS)
        self.assertEqual(rapid.result_date, dt.date())

    def test_rapid_neg(self):
        dt = get_utcnow()
        rapid = Rapid(reference_datetime=get_utcnow(), result=NEG, result_date=dt)
        self.assertEqual(rapid.result, NEG)
        self.assertEqual(rapid.result_date, dt.date())

    def test_rapid_none(self):
        rapid = Rapid()
        self.assertEqual(rapid.result, None)
        self.assertEqual(rapid.result_date, None)

    def test_rapid_missing_date(self):
        rapid = Rapid(reference_datetime=get_utcnow(), result=POS)
        self.assertEqual(rapid.result, None)
        self.assertEqual(rapid.result_date, None)

    def test_result_neg_timing(self):
        """Assert NEG until past 3m, then None."""
        rapid = Rapid(
            reference_datetime=get_utcnow(),
            result_date=(get_utcnow() - relativedelta(months=0)).date(),
            result=NEG)
        self.assertEqual(rapid.result, NEG)
        rapid = Rapid(
            reference_datetime=get_utcnow(),
            result_date=(get_utcnow() - relativedelta(months=1)).date(),
            result=NEG)
        self.assertEqual(rapid.result, NEG)
        rapid = Rapid(
            reference_datetime=get_utcnow(),
            result_date=(get_utcnow() - relativedelta(months=2)).date(),
            result=NEG)
        self.assertEqual(rapid.result, NEG)
        rapid = Rapid(
            reference_datetime=get_utcnow(),
            result_date=(get_utcnow() - relativedelta(months=3)).date(),
            result=NEG)
        self.assertEqual(rapid.result, None)
        rapid = Rapid(
            reference_datetime=get_utcnow(),
            result_date=(get_utcnow() - relativedelta(months=4)).date(),
            result=NEG)
        self.assertEqual(rapid.result, None)


class TestCurrent(TestCase):

    def test_pos_with_evidence(self):
        """Assert POS from recent class with evidence is POS."""
        dt = get_utcnow().date()
        current = Current(
            reference_datetime=get_utcnow(),
            result=POS, result_date=dt, evidence=YES)
        self.assertEqual(current.result, POS)

    def test_none_without_evidence(self):
        """Assert POS from recent class with evidence is POS, else None."""
        dt = get_utcnow().date()
        current = Current(
            reference_datetime=get_utcnow(),
            result=POS, result_date=dt, evidence=YES)
        self.assertEqual(current.result, POS)
        current = Current(
            reference_datetime=get_utcnow(),
            result=POS, result_date=dt, evidence=NO)
        self.assertEqual(current.result, None)

    def test_none_if_neg(self):
        """Assert NEG from recent class with/without evidence is None."""
        dt = get_utcnow().date()
        current = Current(
            reference_datetime=get_utcnow(),
            result=NEG, result_date=dt, evidence=NO)
        self.assertEqual(current.result, None)
        current = Current(
            reference_datetime=get_utcnow(),
            result=NEG, result_date=dt, evidence=YES)
        self.assertEqual(current.result, None)


class TestRecent(TestCase):

    def test_result_pos(self):
        """Assert POS from recent class with evidence is POS."""
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=get_utcnow().date(),
            result=POS,
            evidence=YES)
        self.assertEqual(recent.result, POS)

    def test_result_pos_without_evidence_is_none(self):
        """Assert POS from recent class with evidence is POS."""
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=get_utcnow().date(),
            result=POS,
            evidence=NO)
        self.assertEqual(recent.result, None)

    def test_result_none_if_not_tested(self):
        """Assert None if no test."""
        recent = Recent(tested=NO)
        self.assertEqual(recent.result, None)

    def test_result_none_if_not_tested2(self):
        """Assert None if no test."""
        recent = Recent()
        self.assertEqual(recent.result, None)

    def test_result_neg_with_evidence(self):
        """Assert NEG from recent class with evidence is NEG."""
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=get_utcnow().date(),
            result=NEG,
            evidence=YES)
        self.assertEqual(recent.result, NEG)

    def test_result_neg_without_evidence(self):
        """Assert NEG from recent class without evidence is still NEG."""
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=get_utcnow().date(),
            result=NEG,
            evidence=NO)
        self.assertEqual(recent.result, None)

    def test_result_neg_4months(self):
        """Assert NEG from recent class 4 months old is None."""
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=(get_utcnow() - relativedelta(months=4)).date(),
            result=NEG,
            evidence=YES)
        self.assertEqual(recent.result, None)

    def test_testeddate_not_within3m(self):
        """Assert .within3m False if testdate 4m ago."""
        date_4m_ago = (get_utcnow() - relativedelta(months=4)).date()
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=date_4m_ago,
            result=POS,
            evidence=YES)
        self.assertEqual(recent.within_3m, False)

    def test_testeddate_within3m_less_day(self):
        """Assert .within3m True if testdate 3m ago less one day."""
        date_3m_ago_less_day = (get_utcnow() - relativedelta(months=3) - relativedelta(days=1)).date()
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=date_3m_ago_less_day,
            result=POS,
            evidence=YES)
        self.assertEqual(recent.within_3m, False)

    def test_testeddate_within3m_exact(self):
        """Assert .within3m False if testdate 3m ago (not inclusive)."""
        date_3m_ago = (get_utcnow() - relativedelta(months=3)).date()
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=date_3m_ago,
            result=POS,
            evidence=YES)
        self.assertEqual(recent.within_3m, False)

    def test_testeddate_within3m_plus_day(self):
        """Assert .within3m False if testdate 3m ago + day."""
        date_3m_ago_plus_day = (get_utcnow() - relativedelta(months=3) + relativedelta(days=1)).date()
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=date_3m_ago_plus_day,
            result=POS,
            evidence=YES)
        self.assertEqual(recent.within_3m, True)

    def test_testeddate_within3m_less_month(self):
        """Assert .within3m False if testdate 3m ago + day."""
        date_2m_ago = (get_utcnow() - relativedelta(months=2)).date()
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=date_2m_ago,
            result=POS,
            evidence=YES)
        self.assertEqual(recent.within_3m, True)

    def test_result_neg_timing(self):
        """Assert NEG until past 3m, then None."""
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=(get_utcnow() - relativedelta(months=0)).date(),
            result=NEG,
            evidence=YES)
        self.assertEqual(recent.result, NEG)
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=(get_utcnow() - relativedelta(months=1)).date(),
            result=NEG,
            evidence=YES)
        self.assertEqual(recent.result, NEG)
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=(get_utcnow() - relativedelta(months=2)).date(),
            result=NEG,
            evidence=YES)
        self.assertEqual(recent.result, NEG)
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=(get_utcnow() - relativedelta(months=3)).date(),
            result=NEG,
            evidence=YES)
        self.assertEqual(recent.result, None)
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=(get_utcnow() - relativedelta(months=4)).date(),
            result=NEG,
            evidence=YES)
        self.assertEqual(recent.result, None)


class TestEnrollment(TestCase):

    def test_neg(self):
        dt = get_utcnow()
        current = Current(
            reference_datetime=get_utcnow(),
            result=None, result_date=None, evidence=None)
        self.assertEqual(current.result, None)
        recent = Recent(
            reference_datetime=get_utcnow(),
            tested=YES,
            result_date=dt - relativedelta(weeks=4),
            result=NEG,
            evidence=YES)
        self.assertEqual(recent.result, NEG)
        rapid = Rapid(reference_datetime=get_utcnow(), result=NEG, result_date=dt)
        self.assertEqual(rapid.result, NEG)
        enrollment = EnrollmentResult(
            reference_datetime=get_utcnow(),
            current=current, recent=recent, rapid=rapid)
        self.assertEqual(enrollment.result, NEG)

    def test_raises_rapid_required(self):
        """Asserts a None result raises an exception."""
        current = Current(
            reference_datetime=get_utcnow(),
            result=None, result_date=None, evidence=None)
        self.assertEqual(current.result, None)
        self.assertRaises(RapidTestRequiredError, EnrollmentResult, current=current, recent=None, rapid=None)

    def test_pos(self):
        current = Current(
            reference_datetime=get_utcnow(),
            result=POS, result_date=get_utcnow().date(), evidence=YES)
        self.assertEqual(current.result, POS)
        enrollment = EnrollmentResult(
            reference_datetime=get_utcnow(),
            current=current, recent=None, rapid=None)
        self.assertEqual(enrollment.result, POS)


class TestPostEnrollmentResult(TestCase):

    def test_enrolled_neg_rapid_ind_1m(self):
        """Asserts raises exception is result is IND."""
        dt = get_utcnow()
        result_date = (dt - relativedelta(months=5)).date()
        rapid_results = (
            Test(tested=YES, result=IND, result_date=dt - relativedelta(months=1)),
        )
        self.assertRaises(
            ElisaRequiredError,
            PostEnrollmentResult,
            reference_datetime=dt,
            enrollment_result=Test(result=NEG, result_date=result_date, tested=YES),
            rapid_results=rapid_results)

    def test_enrolled_neg_rapid_ind_3m(self):
        """Asserts raises ElisaRequiredError exception if rapid result is IND within 3 months."""
        dt = get_utcnow()
        result_date = (dt - relativedelta(months=2)).date()
        rapid_results = (
            Test(tested=YES, result=IND, result_date=dt - relativedelta(months=1)),
        )
        self.assertRaises(
            ElisaRequiredError, PostEnrollmentResult,
            reference_datetime=dt,
            enrollment_result=Test(result=NEG, result_date=result_date, tested=YES),
            rapid_results=rapid_results)

    def test_enrolled_neg_rapid_ind_4m(self):
        """Asserts returns None for old NEG, IND results."""
        dt = get_utcnow()
        result_date = (dt - relativedelta(months=5)).date()
        rapid_results = (
            Test(tested=YES, result=IND, result_date=dt - relativedelta(months=4)),
        )
        post_enrollment_result = PostEnrollmentResult(
            reference_datetime=dt,
            enrollment_result=Test(result=NEG, result_date=result_date, tested=YES),
            rapid_results=rapid_results)
        self.assertEquals(post_enrollment_result.result, None)
        self.assertEquals(post_enrollment_result.result_date, None)

    def test_enrolled_neg_still_neg_no_rapid_2m(self):
        dt = get_utcnow()
        result_date = (dt - relativedelta(months=2)).date()
        rapid_results = ()
        post_enrollment_result = PostEnrollmentResult(
            reference_datetime=dt,
            enrollment_result=Test(result=NEG, result_date=result_date, tested=YES),
            rapid_results=rapid_results)
        self.assertEquals(post_enrollment_result.result, NEG)
        self.assertEquals(post_enrollment_result.result_date, result_date)

    def test_enrolled_neg_still_neg_no_rapid_3m(self):
        dt = get_utcnow()
        result_date = (dt - relativedelta(months=3)).date()
        rapid_results = ()
        post_enrollment_result = PostEnrollmentResult(
            reference_datetime=dt,
            enrollment_result=Test(result=NEG, result_date=result_date, tested=YES),
            rapid_results=rapid_results)
        self.assertEquals(post_enrollment_result.result, None)
        self.assertEquals(post_enrollment_result.result_date, None)

    def test_enrolled_neg_still_neg_no_rapid_4m(self):
        dt = get_utcnow()
        result_date = (dt - relativedelta(months=4)).date()
        rapid_results = ()
        post_enrollment_result = PostEnrollmentResult(
            reference_datetime=dt,
            enrollment_result=Test(result=NEG, result_date=result_date, tested=YES),
            rapid_results=rapid_results)
        self.assertEquals(post_enrollment_result.result, None)
        self.assertEquals(post_enrollment_result.result_date, None)

    def test_enrolled_neg_still_neg(self):
        dt = get_utcnow()
        rapid_results = (
            Test(tested=YES, result=NEG, result_date=dt - relativedelta(months=4)),
            Test(tested=YES, result=NEG, result_date=dt - relativedelta(months=3)),
            Test(tested=YES, result=NEG, result_date=dt - relativedelta(months=2)),
        )
        post_enrollment_result = PostEnrollmentResult(
            reference_datetime=dt,
            enrollment_result=Test(result=NEG, result_date=(dt - relativedelta(months=4)).date(), tested=YES),
            rapid_results=rapid_results)
        self.assertEquals(post_enrollment_result.result, NEG)
        self.assertEquals(post_enrollment_result.result_date, (dt - relativedelta(months=2)).date())

    def test_enrolled_neg_now_pos(self):
        dt = get_utcnow()
        rapid_results = (
            Test(tested=YES, result=POS, result_date=dt - relativedelta(months=4)),
            Test(tested=YES, result=UNK, result_date=dt - relativedelta(months=3)),
            Test(tested=YES, result=UNK, result_date=dt - relativedelta(months=2)),
        )
        post_enrollment_result = PostEnrollmentResult(
            reference_datetime=dt,
            enrollment_result=Test(tested=YES, result=NEG, result_date=dt - relativedelta(months=4)),
            rapid_results=rapid_results)
        self.assertEquals(post_enrollment_result.result, POS)
        self.assertEquals(post_enrollment_result.result_date, (dt - relativedelta(months=4)).date())

    def test_enrolled_neg_now_pos2(self):
        dt = get_utcnow()
        rapid_results = (
            Test(tested=YES, result=NEG, result_date=dt - relativedelta(months=4)),
            Test(tested=YES, result=POS, result_date=dt - relativedelta(months=3)),
            Test(tested=YES, result=UNK, result_date=dt - relativedelta(months=2)),
        )
        post_enrollment_result = PostEnrollmentResult(
            reference_datetime=dt,
            enrollment_result=Test(tested=YES, result=NEG, result_date=dt - relativedelta(months=4)),
            rapid_results=rapid_results)
        self.assertEquals(post_enrollment_result.result, POS)
        self.assertEquals(post_enrollment_result.result_date, (dt - relativedelta(months=3)).date())

    def test_enrolled_neg_now_pos3(self):
        dt = get_utcnow()
        rapid_results = (
            Test(tested=YES, result=NEG, result_date=dt - relativedelta(months=4)),
            Test(tested=YES, result=UNK, result_date=dt - relativedelta(months=3)),
            Test(tested=YES, result=POS, result_date=dt - relativedelta(months=2)),
        )
        post_enrollment_result = PostEnrollmentResult(
            reference_datetime=dt,
            enrollment_result=Test(tested=YES, result=NEG, result_date=dt - relativedelta(months=4)),
            rapid_results=rapid_results)
        self.assertEquals(post_enrollment_result.result, POS)
        self.assertEquals(post_enrollment_result.result_date, (dt - relativedelta(months=2)).date())

    def test_enrolled_pos_always_pos(self):
        dt = get_utcnow()
        result_date = (dt - relativedelta(months=4)).date()
        rapid_results = (
            Test(tested=YES, result=UNK, result_date=dt - relativedelta(months=4)),
            Test(tested=YES, result=UNK, result_date=dt - relativedelta(months=3)),
            Test(tested=YES, result=UNK, result_date=dt - relativedelta(months=2)),
        )
        post_enrollment_result = PostEnrollmentResult(
            reference_datetime=dt,
            enrollment_result=Test(tested=YES, result=POS, result_date=result_date),
            rapid_results=rapid_results)
        self.assertEquals(post_enrollment_result.result, POS)
        self.assertEquals(post_enrollment_result.result_date, result_date)
