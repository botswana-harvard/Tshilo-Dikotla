from django.test import TestCase, tag

from edc_constants.constants import (YES, NO)

from td_list.models import AdultDiagnoses, WhoAdultDiagnosis
from td_maternal.forms import MaternalDiagnosisForm

from .test_mixins import PosMotherMixin


@tag('postenrollment', 'forms')
class TestMaternalDiagnosisForm(PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalDiagnosisForm, self).setUp()

        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M', '1020M')
        maternal_visit = self.get_maternal_visit('1020M')

        self.diagnoses = AdultDiagnoses.objects.create(
            name="Gestational Hypertension",
            short_name="Gestational Hypertension")

        self.diagnoses_na = AdultDiagnoses.objects.create(
            name="Not Applicable",
            short_name="N/A")

        self.who_dx = WhoAdultDiagnosis.objects.create(
            short_name="Recurrent severe bacterial pneumo",
            name="Recurrent severe bacterial pneumonia")

        self.who_dx_na = WhoAdultDiagnosis.objects.create(
            short_name="N/A",
            name="Not Applicable")

        self.options = {
            'maternal_visit': maternal_visit.id,
            'new_diagnoses': YES,
            'diagnoses': [self.diagnoses.id],
            'has_who_dx': YES,
            'who': [self.who_dx.id]}

    def test_has_diagnoses_no_dx(self):
        self.options['diagnoses'] = None
        form = MaternalDiagnosisForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has new diagnoses, please give a diagnosis.', errors)

    def test_has_diagnoses_not_applicable_selected(self):
        self.options['diagnoses'] = [self.diagnoses.id, self.diagnoses_na.id]
        form = MaternalDiagnosisForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('New Diagnoses is Yes, diagnoses list cannot have Not Applicable. Please correct.', errors)

    def test_has_no_dx_but_listed(self):
        self.options['new_diagnoses'] = NO
        form = MaternalDiagnosisForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant does not have any new diagnoses, new diagnosis should be Not Applicable.', errors)

    def test_has_no_dx_but_listed_with_not_applicable(self):
        self.options['new_diagnoses'] = NO
        self.options['diagnoses'] = [self.diagnoses.id, self.diagnoses_na.id]
        form = MaternalDiagnosisForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant does not have any new diagnoses, new diagnosis should be Not Applicable.', errors)

    def test_has_who_diagnosis(self):
        self.options['who'] = None
        form = MaternalDiagnosisForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('WHO diagnosis is Yes, please give who diagnosis.', errors)

    def test_has_who_diagnosis_not_applicable_selected(self):
        self.options['who'] = [self.who_dx.id, self.who_dx_na.id]
        form = MaternalDiagnosisForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('WHO Stage III/IV cannot have Not Applicable in the list. Please correct.', errors)

    def test_has_now_who_dx_but_listed(self):
        self.options['has_who_dx'] = NO
        form = MaternalDiagnosisForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'WHO diagnoses is {}, WHO Stage III/IV should be Not Applicable.'.format(self.options['has_who_dx']),
            errors)
