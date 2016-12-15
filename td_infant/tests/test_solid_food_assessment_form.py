from django.test import TestCase

from td_list.models import Foods

from edc_constants.constants import POS, YES, OTHER

from td_infant.forms import SolidFoodAssessementForm
from .test_mixins import InfantMixin


class TestSolidFoodAssessementForm(InfantMixin, TestCase):

    def setUp(self):
        super(TestSolidFoodAssessementForm, self).setUp()
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000', '2010', '2020')
        self.infant_visit = self.get_infant_visit('2020')

        self.solid_foods = Foods.objects.create(
            name=OTHER, short_name=OTHER, display_index=7, field_name=None,
            version="1.0", created="2016-07-28T11:08:56.576", modified="2016-07-28T11:08:56.576", user_created="",
            user_modified="", hostname_created="bcpp025", hostname_modified="bcpp025",
            revision="dev01-stable-147-g6f81e43:develop:6f81e431218ceb2eaa080f81705d4cacbd83aea8")

        self.options = {'age_solid_food': 7,
                        'solid_foods': [self.solid_foods.id],
                        'solid_foods_other': None,
                        'porridge': YES,
                        'porridge_freq': 5,
                        'tsabana': YES,
                        'tsabana_week': 5,
                        'mother_tsabana': YES,
                        'meat': YES,
                        'meat_freq': 5,
                        'potatoes': YES,
                        'potatoes_freq': 5,
                        'carrot_swt_potato': YES,
                        'carrot_swt_potato_freq': 5,
                        'green_veg': YES,
                        'green_veg_freq': 5,
                        'fresh_fruits': YES,
                        'fresh_fruits_freq': 5,
                        'fullcream_milk': YES,
                        'fullcream_milk_freq': 5,
                        'skim_milk': YES,
                        'skim_milk_freq': 5,
                        'raw_milk': YES,
                        'raw_milk_freq': 5,
                        'juice': YES,
                        'juice_freq': 5,
                        'eggs': YES,
                        'eggs_freq': 5,
                        'yogurt': YES,
                        'yogurt_freq': 5,
                        'cheese': YES,
                        'cheese_freq': 5,
                        'rations': YES,
                        'rations_receviced ': '',
                        }

    def test_validate_other_solid_food_assessment_other_specified(self):
        """Test if other is specified if selected other"""
        self.options.update(solid_foods_other=None)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('You selected Other foods, Please specify',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_had_any_poridge(self):
        """Test if the child had any porridge"""
        self.options['porridge'] = YES
        self.options['porridge_freq'] = 0
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question6: Please indicate how many times this child has had porridge in the last week',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_had_any_tsabana(self):
        """Test if the child had any tsabana"""
        self.options.update(tsabana=YES, tsabana_week=0,)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question8: Please indicate how many times this child has had tsabana in the last week',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_has_the_child_had_meat_chicken_or_fish(self):
        """Test Since this time yesterday, has this child had any meat, chicken or fish"""
        self.options.update(meat=YES, meat_freq=0)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question11: Please indicate how many times the child has had any meat, chicken or fish',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_has_the_child_had_any_potatoes(self):
        """Test since this time yesterday, has this child had any potatoes"""
        self.options.update(potatoes=YES, potatoes_freq=0)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question13: Please indicate how many times the child has had any potatoes',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_has_had_carrot_swt_potato(self):
        """Test if child has had pumpkin, carrot or sweet potato"""
        self.options.update(carrot_swt_potato=YES, carrot_swt_potato_freq=0)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question15: Please indicate how many times this child has had carrot, pumpkin or sweet potato',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_has_had_green_veg(self):
        """Test if child has had green vegetables"""
        self.options.update(green_veg=YES, green_veg_freq=0)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question17: Please indicate how many times this child has had green vegetables in the last week',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_has_had_fresh_fruits(self):
        """Test child has had fresh fruits"""
        self.options.update(fresh_fruits=YES, fresh_fruits_freq=0)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question19: Please indicate how many times this child has had fresh fruits in the last week',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_has_had_full_cream_milk(self):
        """Test if child has had fullcream milk"""
        self.options.update(fullcream_milk=YES, fullcream_milk_freq=0)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question21: Please indicate how many times this child has had full cream milk in the last week',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_has_had_skim_milk(self):
        """Test if child has had skim milk"""
        self.options.update(skim_milk=YES, skim_milk_freq=0)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question23: Please indicate how many times this child has had skim milk in the last week',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_has_had_raw_milk(self):
        """Test if child has had raw milk"""
        self.options.update(raw_milk=YES, raw_milk_freq=0)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question25: Please indicate how many times this child has had raw milk in the last week',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_has_had_juice(self):
        """Test if child has had juice"""
        self.options.update(juice=YES, juice_freq=0)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question27: Please indicate how many times this child has had juice in the last week',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_has_had_eggs(self):
        """ Test if child has had eggs"""
        self.options.update(eggs=YES, eggs_freq=0)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question29: Please indicate how many times this child has had eggs in the last week',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_has_had_yogurt(self):
        """Test if child has had yogurt"""
        self.options.update(yogurt=YES, yogurt_freq=0)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question31: Please indicate how many times this child has had yogurt in the last week',
                      solid_foods_form.errors.get('__all__'))

    def test_validate_has_had_cheese(self):
        """Test if child has had cheese"""
        self.options.update(cheese=YES, cheese_freq=0)
        solid_foods_form = SolidFoodAssessementForm(data=self.options)
        self.assertIn('Question33: Please indicate how many times this child has had Cheese in the last week',
                      solid_foods_form.errors.get('__all__'))
