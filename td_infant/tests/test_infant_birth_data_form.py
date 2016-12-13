from django import forms
from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NO

from td_infant.forms import InfantBirthDataForm
from td_infant.tests.test_mixins import InfantMixin


class TestInfantBirthData(InfantMixin, TestCase):

    def setUp(self):
        super(TestInfantBirthData, self).setUp()
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visit('2000', 'scheduled')
        infant_visit = self.get_infant_visit('2000')
        self.options = {
            'report_datetime': get_utcnow(),
            'infant_visit': infant_visit,
            'weight_kg': 3.61,
            'infant_length': 89.97,
            'head_circumference': 39.30,
            'apgar_score': NO,
            'apgar_score_min_1': '',
            'apgar_score_min_5': '',
            'apgar_score_min_10': '',
            'congenital_anomalities': NO}

    def test_infant_length(self):
            self.options.update(infant_length=95.62)
            self.assertRaises(forms.ValidationError)

    def test_validate_infant_head_cir(self):
        self.options.update(head_circumference=41.23)
        self.assertRaises(forms.ValidationError)

    def test_validate_apgar_1(self):
        self.options.update(apgar_score=YES)
        form = InfantBirthDataForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If Apgar scored performed, then you should answer At 1 minute', errors)

    def test_validate_apgar_2(self):
        self.options.update(apgar_score=YES)
        form = InfantBirthDataForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If Apgar scored performed, then you should answer At 1 minute', errors)

    def test_validate_apgar_3(self):
        self.options.update(
            apgar_score=YES,
            apgar_score_min_1=3)
        form = InfantBirthDataForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If Apgar scored performed, then you should answer At 5 minute', errors)

    def test_validate_apgar_4(self):
        self.options.update(
            apgar_score=NO,
            apgar_score_min_1=3)
        form = InfantBirthDataForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If Apgar scored was NOT performed, then you should NOT answer at 1 minute', errors)

    def test_validate_apgar_5(self):
        self.options.update(
            apgar_score=NO,
            apgar_score_min_5=3)
        form = InfantBirthDataForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If Apgar scored was NOT performed, then you should NOT answer at 5 minute', errors)

    def test_validate_apgar_6(self):
        self.options.update(
            apgar_score=NO,
            apgar_score_min_10=3)
        form = InfantBirthDataForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If Apgar scored was NOT performed, then you should NOT answer at 10 minute', errors)
