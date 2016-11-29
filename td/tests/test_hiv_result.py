from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NEG, NO

from dateutil.relativedelta import relativedelta

from ..hiv_result import Recent, Current, Rapid


class Obj:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.report_datetime = get_utcnow()


class TestRapid(TestCase):

    def test_rapid_pos(self):
        dt = get_utcnow()
        rapid = Rapid(tested=YES, result=POS, result_date=dt)
        self.assertEqual(rapid.result, POS)
        self.assertEqual(rapid.date, dt.date())

    def test_rapid_pos_no_evidence_is_none(self):
        rapid = Rapid(tested=NO, result=POS, result_date=get_utcnow())
        self.assertEqual(rapid.result, None)
        self.assertEqual(rapid.date, None)

    def test_rapid_neg(self):
        dt = get_utcnow()
        rapid = Rapid(tested=YES, result=NEG, result_date=dt)
        self.assertEqual(rapid.result, NEG)
        self.assertEqual(rapid.date, dt.date())

    def test_rapid_neg_no_evidence_is_none(self):
        rapid = Rapid(tested=NO, result=POS, result_date=get_utcnow())
        self.assertEqual(rapid.result, None)
        self.assertEqual(rapid.date, None)

    def test_rapid_none(self):
        rapid = Rapid()
        self.assertEqual(rapid.result, None)
        self.assertEqual(rapid.date, None)

    def test_rapid_missing_date(self):
        rapid = Rapid(tested=YES, result=POS)
        self.assertEqual(rapid.result, None)
        self.assertEqual(rapid.date, None)


class TestCurrent(TestCase):

    def test_pos_with_evidence(self):
        """Assert POS from recent class with evidence is POS."""
        current = Current(result=POS, evidence=YES)
        self.assertEqual(current.result, POS)

    def test_none_without_evidence(self):
        """Assert POS from recent class with evidence is POS, else None."""
        current = Current(result=POS, evidence=YES)
        self.assertEqual(current.result, POS)
        current = Current(result=POS, evidence=NO)
        self.assertEqual(current.result, None)

    def test_none_if_neg(self):
        """Assert NEG from recent class with/without evidence is None."""
        current = Current(result=NEG, evidence=NO)
        self.assertEqual(current.result, None)
        current = Current(result=NEG, evidence=YES)
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
            evidence=NO)
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
