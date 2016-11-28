import unittest

from ..pregnancy_calculator import Edd, Lmp, Ultrasound
from edc_base.utils import get_utcnow
from dateutil.relativedelta import relativedelta


class TestPregnancyCalculations(unittest.TestCase):

    def test_lmp(self):
        dt = get_utcnow()
        self.assertEqual(dt - relativedelta(days=280), Lmp(dt).edd)
