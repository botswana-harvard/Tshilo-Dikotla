from dateutil.relativedelta import relativedelta
from django.utils import timezone
from model_mommy import mommy

from edc_constants.constants import UNKNOWN, YES, NEG, NOT_APPLICABLE, NO, POS
from td.models import Appointment

from td_maternal.forms import MaternalClinicalMeasurementsTwoForm

from .base_test_case import BaseTestCase
from edc_visit_tracking.constants import SCHEDULED

from ..mommy_recipes import fake


class TestMaternalClinicalMeasurementsTwo(BaseTestCase):

    def setUp(self):
        super(TestMaternalClinicalMeasurementsTwo, self).setUp()

        self.options = {
            'maternal_visit': self.antenatal_visit_1_pos,
            'weight_kg': 76,
            'systolic_bp': 120,
            'diastolic_bp': 100}

    def test_diastolic_not_higher_than_systolic(self):
        """Test whether the Systolic Blood Pressure is not lower than the Diastolic Pressure"""
        self.options.update(
            systolic_bp=100,
            diastolic_bp=120)
        form = MaternalClinicalMeasurementsTwoForm(data=self.options)
        self.assertIn(
            'Systolic blood pressure cannot be lower than the diastolic blood pressure.'
            ' Please correct.', form.errors.get('__all__'))

    def test_systolic_not_blank(self):
        """Test if the Systolic blood pressure field is not empty"""
        self.options.update(systolic_bp=None)
        form = MaternalClinicalMeasurementsTwoForm(data=self.options)
        self.assertIn('Systolic Blood Pressure field cannot be blank. Please correct', form.errors.get('__all__'))

    def test_diastolic_not_blank(self):
        """Test if the Diastolic pressure field is blank"""
        self.options.update(diastolic_bp=None)
        form = MaternalClinicalMeasurementsTwoForm(data=self.options)
        self.assertIn('Diastolic Blood Pressure field cannot be blank. Please correct', form.errors.get('__all__'))
