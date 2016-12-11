from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.test.utils import tag

from edc_constants.constants import POS, NEG

from ..maternal_hiv_status import MaternalHivStatus

from .test_mixins import PosMotherMixin
from td_maternal.tests.test_mixins import MotherMixin, RAPID, ENROLLMENT, RECENT
from edc_base.test_mixins import TestMixinError


@tag('pos')
class TestMaternalHivStatusPos(PosMotherMixin, TestCase):
    """Tests where the mother is POS."""

    def setUp(self):
        super(TestMaternalHivStatusPos, self).setUp()
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M', '1020M')

    def test_pos_status_anytime(self):
        """Asserts can determine POS at any visit."""
        maternal_visit = self.add_maternal_visit('1010M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, POS)
        self.make_delivery()
        maternal_visit = self.add_maternal_visit('2000M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, POS)
        maternal_visit = self.add_maternal_visit('2010M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, POS)
        maternal_visit = self.add_maternal_visit('2020M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, POS)


@tag('neg')
class TestMaternalHivStatusNeg(MotherMixin, TestCase):

    def test_neg_status_enrollment(self):
        """Asserts "current" NEG status reported at enrollment requires rapid."""
        self.assertRaises(
            TestMixinError,
            self.make_negative_mother, use_result=ENROLLMENT)

    def test_neg_status_recent(self):
        """Asserts NEG result at enrollment requires rapid."""
        self.make_negative_mother(use_result=RECENT)
        maternal_visit = self.add_maternal_visit('1000M')
        # rapid test date is 4 weeks prior to enrollment, so add 2 months
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime + relativedelta(months=2))
        self.assertEqual(maternal_hiv_status.result, NEG)
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime + relativedelta(months=3))
        self.assertEqual(maternal_hiv_status.result, None)

    def test_neg_status_valid_for_only_3m(self):
        """Asserts NEG result from enrollment only valid for 3m"""
        self.make_negative_mother(use_result=RAPID)
        maternal_visit = self.add_maternal_visit('1000M')
        # rapid test date is 4 weeks prior to enrollment, so add 2 months
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime + relativedelta(months=2))
        self.assertEqual(maternal_hiv_status.result, NEG)
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime + relativedelta(months=3))
        self.assertEqual(maternal_hiv_status.result, None)

    def test_seroconversion(self):
        """Assert POS by rapid test overrides NEG from enrollment."""
        self.make_negative_mother(use_result=RAPID)
        self.add_maternal_visits('1000M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=self.get_last_maternal_visit().report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M', '1020M')
        self.make_delivery()
        self.add_maternal_visits('2000M', '2010M', '2020M', '2060M')
        self.make_rapid_test(result=POS)
        maternal_visit = self.get_maternal_visit('2060M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, POS)

    def test_neg_status_from_rapid_test(self):
        """Assert Rapid test is used to determine status"""
        self.make_negative_mother(use_result=RAPID)
        maternal_visit = self.add_maternal_visit('1000M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        self.make_antenatal_enrollment_two()
        self.add_maternal_visit('1010M')
        maternal_visit = self.add_maternal_visit('1020M')  # 4 months, enrollment result no longer valid
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, None)
        self.make_delivery()
        self.add_maternal_visit('2000M')
        self.make_rapid_test(result=NEG)
        self.add_maternal_visit('2010M')
        maternal_visit = self.add_maternal_visit('2020M')
        # Visit within 3months of rapid test.
        self.assertLessEqual(
            relativedelta(
                self.get_maternal_visit('2020M').report_datetime,
                self.get_maternal_visit('2000M').report_datetime).months, 3)
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)

    def test_add_rapid_but_too_old(self):
        """Assert NEG rapid older than 3months will not change result."""
        self.make_negative_mother(use_result=RAPID)
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M', '1020M')
        self.make_delivery()
        self.add_maternal_visits('2000M', '2010M', '2020M')
        maternal_visit = self.get_maternal_visit('2020M')
        self.make_rapid_test(
            visit=maternal_visit,
            result=NEG,
            result_date=(maternal_visit.report_datetime - relativedelta(months=4)).date())
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=maternal_visit.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, None)
