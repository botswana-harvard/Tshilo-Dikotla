from django import forms

from edc_constants.constants import YES, NO, UNKNOWN
from ..models import SolidFoodAssessment

from .base_infant_model_form import BaseInfantModelForm


class SolidFoodAssessementForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(SolidFoodAssessementForm, self).clean()
        self.validate_had_any_poridge()
        self.validate_had_any_tsabana()
        self.validate_has_the_child_had_meat_chicken_or_fish()
        self.validate_has_the_child_had_any_potatoes()
        self.validate_has_had_carrot_swt_potato()
        self.validate_has_had_green_veg()
        self.validate_has_had_fresh_fruits()
        self.validate_has_had_full_cream_milk()
        self.validate_has_had_skim_milk()
        self.validate_has_had_raw_milk()
        self.validate_has_had_juice()
        self.validate_has_had_eggs()
        self.validate_has_had_yogurt()
        self.validate_has_had_cheese()
        # self.validate_other_solid_food_assessment_specified()
        return cleaned_data

    def validate_had_any_poridge(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('porridge') == YES:
            if not cleaned_data.get('porridge_freq'):
                raise forms.ValidationError(
                    'Question6: Please indicate how many times this child has had porridge in the last week')

    def validate_had_any_tsabana(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('tsabana') == YES:
            if not cleaned_data.get('tsabana_week'):
                raise forms.ValidationError(
                    'Question8: Please indicate how many times this child has had tsabana in the last week')

    def validate_has_the_child_had_meat_chicken_or_fish(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('meat') == YES:
            if not cleaned_data.get('meat_freq'):
                raise forms.ValidationError(
                    'Question11: Please indicate how many times the child has had any meat, chicken or fish')

    def validate_has_the_child_had_any_potatoes(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('potatoes') == YES:
            if not cleaned_data.get('potatoes_freq'):
                raise forms.ValidationError(
                    'Question13: Please indicate how many times the child has had any potatoes')

    def validate_has_had_carrot_swt_potato(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('carrot_swt_potato') == YES:
            if not cleaned_data.get('carrot_swt_potato_freq'):
                raise forms.ValidationError(
                    'Question15: Please indicate how many times this child has had carrot, pumpkin or sweet potato')

    def validate_has_had_green_veg(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('green_veg') == YES:
            if not cleaned_data.get('green_veg_freq'):
                raise forms.ValidationError(
                    'Question17: Please indicate how many times this child has had green vegetables in the last week')

    def validate_has_had_fresh_fruits(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('fresh_fruits') == YES:
            if not cleaned_data.get('fresh_fruits_freq'):
                raise forms.ValidationError(
                    'Question19: Please indicate how many times this child has had fresh fruits in the last week')

    def validate_has_had_full_cream_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('fullcream_milk') == YES:
            if not cleaned_data.get('fullcream_milk_freq'):
                raise forms.ValidationError(
                    'Question21: Please indicate how many times this child has had full cream milk in the last week')

    def validate_has_had_skim_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('skim_milk') == YES:
            if not cleaned_data.get('skim_milk_freq'):
                raise forms.ValidationError(
                    'Question23: Please indicate how many times this child has had skim milk in the last week')

    def validate_has_had_raw_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('raw_milk') == YES:
            if not cleaned_data.get('raw_milk_freq'):
                raise forms.ValidationError(
                    'Question25: Please indicate how many times this child has had raw milk in the last week')

    def validate_has_had_juice(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('juice') == YES:
            if not cleaned_data.get('juice_freq'):
                raise forms.ValidationError(
                    'Question27: Please indicate how many times this child has had juice in the last week')

    def validate_has_had_eggs(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('eggs') == YES:
            if not cleaned_data.get('eggs_freq'):
                raise forms.ValidationError(
                    'Question29: Please indicate how many times this child has had eggs in the last week')

    def validate_has_had_yogurt(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('yogurt') == YES:
            if not cleaned_data.get('yogurt_freq'):
                raise forms.ValidationError(
                    'Question31: Please indicate how many times this child has had yogurt in the last week')

    def validate_has_had_cheese(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('cheese') == YES:
            if not cleaned_data.get('cheese_freq'):
                raise forms.ValidationError(
                    'Question33: Please indicate how many times this child has had Cheese in the last week')

    def validate_other_solid_food_assessment_specified(self):
        cleaned_data = self.cleaned_data
        many2many_qs = cleaned_data.get(
            'solid_foods').values_list('short_name', flat=True)
        many2many_list = list(many2many_qs.all())
        if 'Other' in many2many_list and not cleaned_data.get('solid_foods_other'):
            raise forms.ValidationError(
                'You selected Other foods, Please specify')

    class Meta:
        model = SolidFoodAssessment
        fields = '__all__'
