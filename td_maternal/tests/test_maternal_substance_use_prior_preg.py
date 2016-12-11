from django.test import TestCase

from edc_constants.constants import YES, NO

from td_infant.tests.test_mixins import AddVisitInfantMixin

from ..forms import MaternalSubstanceUsePriorPregForm

from .test_mixins import NegMotherMixin


class TestMaternalSubstanceUsePriorPreg(AddVisitInfantMixin, NegMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalSubstanceUsePriorPreg, self).setUp()
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M', '1020M')
        maternal_visit = self.get_maternal_visit('1020M')
        self.options = {
            'maternal_visit': maternal_visit.id,
            'smoked_prior_to_preg': YES,
            'smoking_prior_preg_freq': 'daily',
            'alcohol_prior_pregnancy': YES,
            'alcohol_prior_preg_freq': 'daily',
            'marijuana_prior_preg': YES,
            'marijuana_prior_preg_freq': 'daily',
            'other_illicit_substances_prior_preg': None}

    def test_smoked_prior_to_pregnancy_yes(self):
        self.options['smoking_prior_preg_freq'] = None
        form = MaternalSubstanceUsePriorPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has smoked tobacco prior to this pregnancy, please give a frequency.', errors)

    def test_smoked_prior_to_pregnancy_no(self):
        self.options['smoked_prior_to_preg'] = NO
        form = MaternalSubstanceUsePriorPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has never smoked tobacco prior to this pregnancy, please do not give a frequency.', errors)

    def test_alcohol_prior_pregnancy_yes(self):
        self.options['alcohol_prior_preg_freq'] = None
        form = MaternalSubstanceUsePriorPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has drank alcohol prior this pregnancy, please give a frequency.', errors)

    def test_alcohol_prior_pregnancy_no(self):
        self.options['alcohol_prior_pregnancy'] = NO
        form = MaternalSubstanceUsePriorPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has never drank alcohol prior this pregnancy, please do not give a frequency.', errors)

    def test_marijuana_prior_preg_yes(self):
        self.options['marijuana_prior_preg_freq'] = None
        form = MaternalSubstanceUsePriorPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has smoked marijuana prior to this pregnancy, please give a frequency.', errors)

    def test_marijuana_prior_preg_no(self):
        self.options['marijuana_prior_preg'] = NO
        form = MaternalSubstanceUsePriorPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has never smoked marijuana prior to this pregnancy, please do not give a frequency.', errors)
