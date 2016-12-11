from django.test import TestCase, tag
from model_mommy import mommy

from edc_constants.constants import YES

from ..forms import MaternalRandoForm

from .test_mixins import MotherMixin


@tag('rando')
class TestMaternalRandomization(MotherMixin, TestCase):

    def test_pick_correct_next_randomization_item(self):
        """Test if the next correct randomization item is picked."""
        self.make_positive_mother()
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        maternal_rando = mommy.make_recipe(
            'td_maternal.maternalrando',
            maternal_visit=self.add_maternal_visit('1010M'))
        self.assertEqual(maternal_rando.sid, 1)
        self.make_positive_mother()
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        maternal_rando = mommy.make_recipe(
            'td_maternal.maternalrando',
            maternal_visit=self.add_maternal_visit('1010M'))
        self.assertEqual(maternal_rando.sid, 2)
        self.make_positive_mother()
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        maternal_rando = mommy.make_recipe(
            'td_maternal.maternalrando',
            maternal_visit=self.add_maternal_visit('1010M'))
        self.assertEqual(maternal_rando.sid, 3)

    def test_pos_mother_validation(self):
        self.make_negative_mother()
        maternal_visit = self.add_maternal_visit('1000M')
        options = {
            'maternal_visit': maternal_visit.id,
            'site': 'gaborone',
            'sid': 1,
            'randomization_datetime': maternal_visit.report_datetime,
            'initials': 'CT',
            'dispensed': YES,
            'delivery_clinic': 'PMH'
        }
        form = MaternalRandoForm(data=options)
        self.assertIn('Mother must be HIV(+) to randomize.', form.errors.get('__all__'))
