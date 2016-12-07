from datetime import date
from django.test import TestCase

from edc_constants.constants import YES, NO

from ..forms import NvpDispensingForm

from .mixins import AntenatalVisitsMotherMixin, PosMotherMixin, DeliverMotherMixin


class TestNvpDispensingForm(AntenatalVisitsMotherMixin, DeliverMotherMixin, PosMotherMixin, TestCase):

    def setUp(self):
        super(TestNvpDispensingForm, self).setUp()

        self.add_maternal_visits('1000M', '1010M', '1020M', '2000M')
        maternal_visit = self.get_maternal_visit('2000M')

        self.options = {
            'maternal_visit': maternal_visit,
            'maternal_delivery': self.maternal_lab_del,
            'nvp_admin_date': date.today(),
            'medication_instructions': YES,
            'dose_admin_infant': '1 spoon per day',
            'correct_dose': YES,
            'corrected_dose': None,
            'dose_adjustment': YES,
            'week_2_dose': None
        }

    def test_validate_correct_dose_no(self):
        self.options.update(correct_dose=NO)
        form = NvpDispensingForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If the correct dose was not given, please give the corrected dose.', errors)

    def test_validate_correct_dose_yes(self):
        self.options.update(corrected_dose='dose')
        form = NvpDispensingForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If the correct dose was given, please do not give the corrected dose.', errors)

    def test_week_2_dose_yes(self):
        form = NvpDispensingForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If infant came for a week 2 dose adjustment, please give the week 2 dose.', errors)

    def test_week_2_dose_no(self):
        self.options.update(
            dose_adjustment=NO,
            week_2_dose='2 spoons per day')
        form = NvpDispensingForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'If infant did not come for a week 2 dose adjustment, '
            'please do not give the week 2 dose.', errors)
