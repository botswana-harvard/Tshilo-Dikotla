from dateutil.relativedelta import relativedelta
from django.test import TestCase
from model_mommy import mommy

from td_maternal.forms import MaternalClinicalMeasurementsTwoForm

from .mixins import AntenatalVisitsMotherMixin, PosMotherMixin


class TestMaternalClinicalMeasurementsTwo(AntenatalVisitsMotherMixin, PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalClinicalMeasurementsTwo, self).setUp()

        self.add_maternal_visit('1000M', '1010M')
        maternal_visit = self.get_maternal_visit('1010M')

        self.options = {
            'maternal_visit': maternal_visit.id,
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
