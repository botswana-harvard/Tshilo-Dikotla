from dateutil.relativedelta import relativedelta
from model_mommy import mommy

from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NO, NEG, NOT_APPLICABLE, UNK, IND
from edc_metadata.models import RequisitionMetadata

from td.models import Appointment
from td_infant.tests.test_mixins import AddVisitInfantMixin

from ..maternal_hiv_status import MaternalHivStatus

from .test_mixins import PosMotherMixin, NegMotherMixin, AntenatalVisitsMotherMixin, DeliverMotherMixin


class TestMaternalHivStatusPos(DeliverMotherMixin, AntenatalVisitsMotherMixin, PosMotherMixin, TestCase):
    """Tests where the mother is POS."""

    def setUp(self):
        super(TestMaternalHivStatusPos, self).setUp()
        self.add_maternal_visits('2000M', '2010M')

    def test_pos_status_anytime(self):
        """Asserts can determine POS at any visit."""
        maternal_visit = self.add_maternal_visit('1010M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, POS)
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


class TestMaternalHivStatusNeg(DeliverMotherMixin, AntenatalVisitsMotherMixin, AddVisitInfantMixin,
                               NegMotherMixin, TestCase):

    def test_neg_status_anytime(self):
        """Asserts can determine NEG at any visit."""
        maternal_visit = self.add_maternal_visit('1010M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        maternal_visit = self.add_maternal_visit('2000M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        maternal_visit = self.add_maternal_visit('2010M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        maternal_visit = self.add_maternal_visit('2020M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        maternal_visit = self.add_maternal_visit('2060M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        maternal_visit = self.add_maternal_visit('2120M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)

    def test_pos_status_from_rapid_test(self):
        """Assert POS by rapid test."""
        self.add_maternal_visits('1020M', '2000M', '2010M')
        maternal_visit = self.get_maternal_visit('2010M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        self.add_maternal_visits('2020M', '2060M')
        mommy.make_recipe(
            'td_maternal.rapidtestresult',
            maternal_visit=maternal_visit,
            result=POS)
        maternal_visit = self.get_maternal_visit('2060M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, POS)

    def test_neg_status_from_enrollment(self):
        """test that we can figure out a negative status with just the enrollment status."""
        for code in ['1020M', '2000M', '2010M', '2020M']:
            maternal_visit = self.add_maternal_visit(code)
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)

    def test_neg_status_from_rapid_test(self):
        """test that we can figure out a negative status taking in to consideration rapid tests."""
        self.add_maternal_visits('1020M', '2000M', '2010M')
        maternal_visit = self.get_maternal_visit('2010M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        mommy.make_recipe('td_maternal.rapidtestresult', maternal_visit=maternal_visit, result=NEG)
        # Visit within 3months of rapid test.
        maternal_visit = self.add_maternal_visit('2020M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)

    def test_unknown_status(self):
        """Assert NEG rapid older than 3months will not change result."""
        self.add_maternal_visits('1020M', '2000M', '2010M')
        maternal_visit = self.get_maternal_visit('2010M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=maternal_visit.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
        maternal_visit = self.add_maternal_visit('2020M')
        mommy.make_recipe(
            'td_maternal.rapidtestresult',
            maternal_visit=maternal_visit,
            result_date=(maternal_visit.report_datetime - relativedelta(months=4)).date(),
            result=NEG)
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=maternal_visit.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, None)

    def test_valid_hiv_neg_week32_test_date(self):
        self.add_maternal_visits('1000M', '1010M', '1020M')
        maternal_visit = self.get_maternal_visit('1020M')
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=maternal_visit.report_datetime)
        self.assertEqual(maternal_hiv_status.result, NEG)
