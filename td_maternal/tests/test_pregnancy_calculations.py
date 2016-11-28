import unittest

from ..pregnancy_calculator import Edd, Lmp, Ultrasound
from edc_base.utils import get_utcnow
from dateutil.relativedelta import relativedelta


class TestPregnancyCalculations(unittest.TestCase):

    def test_lmp_edd(self):
        dt = get_utcnow()
        self.assertEqual(dt + relativedelta(days=280), Lmp(dt).edd)

    def test_ultrasound_days_boundaries(self):
        dt = get_utcnow()
        try:
            Ultrasound(dt, ga_weeks=1, ga_days=7)
            self.fail('TypeError not raised!')
        except TypeError:
            pass

        try:
            Ultrasound(dt, ga_weeks=1, ga_days=-1)
            self.fail('TypeError not raised!')
        except TypeError:
            pass

    def test_ultrasound_weeks_boundaries(self):
        dt = get_utcnow()
        try:
            Ultrasound(dt, ga_weeks=-1)
            self.fail('TypeError not raised!')
        except TypeError:
            pass
        try:
            Ultrasound(dt, ga_weeks=0)
            self.fail('TypeError not raised!')
        except TypeError:
            pass
        try:
            Ultrasound(dt, ga_weeks=40)
            self.fail('TypeError not raised!')
        except TypeError:
            pass

    def test_ultrasound_weeks_floor(self):
        dt = get_utcnow()
        for week in range(1, 40):
            for day in range(0, 7):
                ultrasound = Ultrasound(dt, ga_weeks=week, ga_days=day)
                self.assertEqual(week, ultrasound.ga.weeks)
