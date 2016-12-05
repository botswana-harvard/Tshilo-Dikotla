from .base_test_case import BaseTestCase
from model_mommy import mommy

from td_maternal.forms import MaternalClinicalMeasurementsOneForm


class TestMaternalClinicalMeasurementOne(BaseTestCase):

    def setUp(self):
        super(TestMaternalClinicalMeasurementOne, self).setUp()
        self.data = {
            'maternal_visit': self.maternal_visit_1000_pos,
            'systolic_bp': 75,
            'diastolic_bp': 120, }

    def test_systolic_bp_lower_than_diastolic_bp(self):
        self.data.update(
            systolic_bp=40,
            diastolic_bp=80)
        form = MaternalClinicalMeasurementsOneForm(data=self.data)
        self.assertIn('Systolic blood pressure cannot be lower than the diastolic blood pressure.'
                      ' Please correct.', form.errors.get('__all__'))

    def test_systolic_not_blank(self):
        """Test if the Systolic blood pressure field is not empty"""
        self.data.update(systolic_bp=None)
        form = MaternalClinicalMeasurementsOneForm(data=self.data)
        self.assertIn('Systolic Blood Pressure field cannot be blank. Please correct', form.errors.get('__all__'))

    def test_diastolic_not_blank(self):
        """Test if the Diastolic pressure field is blank"""
        self.data.update(diastolic_bp=None)
        form = MaternalClinicalMeasurementsOneForm(data=self.data)
        self.assertIn('Diastolic Blood Pressure field cannot be blank. Please correct', form.errors.get('__all__'))
