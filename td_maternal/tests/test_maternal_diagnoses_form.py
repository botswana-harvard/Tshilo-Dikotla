from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_code_lists.models import WcsDxAdult
from edc_constants.constants import (YES, NO)

from td_list.models import MaternalDiagnoses
from td_maternal.forms import MaternalDiagnosesForm

from .mixins import AntenatalVisitsMotherMixin, PosMotherMixin


class TestMaternalDiagnosesForm(AntenatalVisitsMotherMixin, PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalDiagnosesForm, self).setUp()

        self.add_maternal_visits('1000M', '1010M', '1020M')
        maternal_visit = self.get_maternal_visit('1020M')

        self.diagnoses = MaternalDiagnoses.objects.create(
            hostname_created="django", name="Gestational Hypertension",
            short_name="Gestational Hypertension", created=get_utcnow(),
            user_modified="", modified=get_utcnow(),
            hostname_modified="django", version="1.0",
            display_index=1, user_created="django", field_name=None,
            revision=":develop:")

        self.diagnoses_na = MaternalDiagnoses.objects.create(
            hostname_created="django", name="Not Applicable",
            short_name="N/A", created=get_utcnow(),
            user_modified="", modified=get_utcnow(),
            hostname_modified="django", version="1.0",
            display_index=1, user_created="django", field_name=None,
            revision=":develop:")

        self.who_dx = WcsDxAdult.objects.create(
            hostname_created="cabel", code="CS4003", short_name="Recurrent severe bacterial pneumo",
            created=get_utcnow(), user_modified="", modified=get_utcnow(), hostname_modified="cabel",
            long_name="Recurrent severe bacterial pneumonia", user_created="abelc",
            list_ref="WHO CLINICAL STAGING OF HIV INFECTION 2006", revision=None)

        self.who_dx_na = WcsDxAdult.objects.create(
            hostname_created="cabel", code="CS4002", short_name="N/A",
            created=get_utcnow(), user_modified="",
            modified=get_utcnow(), hostname_modified="cabel",
            long_name="Not Applicable", user_created="abelc",
            list_ref="WHO CLINICAL STAGING OF HIV INFECTION 2006", revision=None)

        self.options = {
            'maternal_visit': maternal_visit,
            'new_diagnoses': YES,
            'diagnoses': [self.diagnoses.id],
            'has_who_dx': YES,
            'who': [self.who_dx.id]}

    def test_has_diagnoses_no_dx(self):
        self.options['diagnoses'] = None
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has new diagnoses, please give a diagnosis.', errors)

    def test_has_diagnoses_not_applicable_selected(self):
        self.options['diagnoses'] = [self.diagnoses.id, self.diagnoses_na.id]
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('New Diagnoses is Yes, diagnoses list cannot have Not Applicable. Please correct.', errors)

    def test_has_no_dx_but_listed(self):
        self.options['new_diagnoses'] = NO
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant does not have any new diagnoses, new diagnosis should be Not Applicable.', errors)

    def test_has_no_dx_but_listed_with_not_applicable(self):
        self.options['new_diagnoses'] = NO
        self.options['diagnoses'] = [self.diagnoses.id, self.diagnoses_na.id]
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant does not have any new diagnoses, new diagnosis should be Not Applicable.', errors)

    def test_has_who_diagnosis(self):
        self.options['who'] = None
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('WHO diagnosis is Yes, please give who diagnosis.', errors)

    def test_has_who_diagnosis_not_applicable_selected(self):
        self.options['who'] = [self.who_dx.id, self.who_dx_na.id]
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('WHO Stage III/IV cannot have Not Applicable in the list. Please correct.', errors)

    def test_has_now_who_dx_but_listed(self):
        self.options['has_who_dx'] = NO
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'WHO diagnoses is {}, WHO Stage III/IV should be Not Applicable.'.format(self.options['has_who_dx']),
            errors)
