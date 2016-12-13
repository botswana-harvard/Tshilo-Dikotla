from dateutil.relativedelta import relativedelta

from django.test import TestCase, tag

from edc_pregnancy_utils.constants import LMP

from ..pregnancy import Pregnancy

from .test_mixins import MotherMixin
import pytz
from datetime import datetime, time


@tag('review')
class TestPregnancy(MotherMixin, TestCase):

    def test_delivered(self):
        self.make_positive_mother()
        self.add_maternal_visit('1000M')
        self.make_antenatal_enrollment_two()
        maternal_ultrasound = self.make_ultrasound()
        self.add_maternal_visits('1010M', '1020M')
        report_datetime = self.get_last_maternal_visit().report_datetime
        delivery_datetime = pytz.utc.localize(datetime.combine(maternal_ultrasound.est_edd_ultrasound, time()))
        self.make_delivery(
            report_datetime=report_datetime,
            delivery_datetime=delivery_datetime)
        pregnancy = Pregnancy(
            self.maternal_identifier,
            reference_datetime=delivery_datetime)
        self.assertEqual(pregnancy.ga_by_lmp, 25)
        self.assertEqual(pregnancy.ga.weeks, 20)
        self.assertEqual(pregnancy.edd.method, LMP)
        self.assertEqual(pregnancy.delivery_datetime, delivery_datetime)
        self.assertEqual(pregnancy.edd.edd, maternal_ultrasound.est_edd_ultrasound)

    def test_not_delivered(self):
        self.make_positive_mother()
        self.add_maternal_visit('1000M')
        self.make_antenatal_enrollment_two()
        maternal_ultrasound = self.make_ultrasound(ga_by_ultrasound_wks=25)
        self.add_maternal_visits('1010M', '1020M')
        pregnancy = Pregnancy(
            self.maternal_identifier,
            reference_datetime=self.get_last_maternal_visit().report_datetime)
        self.assertEqual(pregnancy.ga_by_lmp, 25)
        self.assertEqual(pregnancy.ga.weeks, 25)
        self.assertIsNone(pregnancy.delivery_datetime)
        self.assertEqual(pregnancy.edd.edd, self.antenatal_enrollment.edd_by_lmp)
        self.assertEqual(pregnancy.edd.edd, maternal_ultrasound.est_edd_ultrasound)
        self.assertEqual(pregnancy.edd.method, LMP)

    def test_reference_datetime_before_delivery(self):
        """Asserts ignores delivery if reference datetime before delivery datetime."""
        self.make_positive_mother()
        self.add_maternal_visit('1000M')
        self.make_antenatal_enrollment_two()
        maternal_ultrasound = self.make_ultrasound()
        self.add_maternal_visits('1010M', '1020M')
        report_datetime = self.get_last_maternal_visit().report_datetime
        delivery_datetime = pytz.utc.localize(datetime.combine(maternal_ultrasound.est_edd_ultrasound, time()))
        self.make_delivery(
            report_datetime=report_datetime,
            delivery_datetime=delivery_datetime)
        pregnancy = Pregnancy(
            self.maternal_identifier,
            reference_datetime=delivery_datetime - relativedelta(weeks=4))
        self.assertIsNone(pregnancy.delivery_datetime)
