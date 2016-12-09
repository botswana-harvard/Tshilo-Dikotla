from django.test import TestCase

from edc_constants.constants import YES, NO

from td_infant.tests.test_mixins import AddVisitInfantMixin

from ..forms import MaternalSubstanceUseDuringPregForm

from .test_mixins import AntenatalVisitsMotherMixin, NegMotherMixin


class TestMaternalSubstanceUseDuringPreg(AntenatalVisitsMotherMixin, AddVisitInfantMixin, NegMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalSubstanceUseDuringPreg, self).setUp()
        self.add_maternal_visits('1000M', '1010M', '1020M')
        maternal_visit = self.get_maternal_visit('1020M')
        self.options = {
            'maternal_visit': maternal_visit.pk,
            'smoked_during_pregnancy': YES,
            'smoking_during_preg_freq': 'daily',
            'alcohol_during_pregnancy': YES,
            'alcohol_during_preg_freq': 'daily',
            'marijuana_during_preg': YES,
            'marijuana_during_preg_freq': 'daily',
            'other_illicit_substances_during_preg': None}

    def test_smoked_during_pregnancy_yes(self):
        self.options['smoking_during_preg_freq'] = None
        form = MaternalSubstanceUseDuringPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has smoked tobacco during this pregnancy, please give a frequency.', errors)

    def test_smoked_during_pregnancy_no(self):
        self.options['smoked_during_pregnancy'] = NO
        form = MaternalSubstanceUseDuringPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has never smoked tobacco during this pregnancy, please do not give a frequency.', errors)

    def test_alcohol_during_pregnancy_yes(self):
        self.options['alcohol_during_preg_freq'] = None
        form = MaternalSubstanceUseDuringPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has drank alcohol during this pregnancy, please give a frequency.', errors)

    def test_alcohol_during_pregnancy_no(self):
        self.options['alcohol_during_pregnancy'] = NO
        form = MaternalSubstanceUseDuringPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has never drank alcohol during this pregnancy, please do not give a frequency.', errors)

    def test_marijuana_during_preg_yes(self):
        self.options['marijuana_during_preg_freq'] = None
        form = MaternalSubstanceUseDuringPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has smoked marijuana during this pregnancy, please give a frequency.', errors)

    def test_marijuana_during_preg_no(self):
        self.options['marijuana_during_preg'] = NO
        form = MaternalSubstanceUseDuringPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has never smoked marijuana during this pregnancy, please do not give a frequency.', errors)
