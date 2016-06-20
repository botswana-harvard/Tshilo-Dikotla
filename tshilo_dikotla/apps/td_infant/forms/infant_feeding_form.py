from django import forms

from edc_constants.constants import YES

from .base_infant_model_form import BaseInfantModelForm
from ..models import InfantFeeding


class InfantFeedingForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantFeedingForm, self).clean()
        self.validate_other_feeding()
        self.validate_took_formula()
        self.validate_cows_milk()
        self.validate_formula_intro_occur(cleaned_data)
        return cleaned_data

    def validate_other_feeding(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('other_feeding') == YES:
            if not cleaned_data.get('formula_intro_date'):
                raise forms.ValidationError('If received formula milk | foods | liquids since last'
                                            ' attended visit. Please provide intro date')
        else:
            if cleaned_data.get('formula_intro_date'):
                raise forms.ValidationError('You mentioned no formula milk | foods | liquids received'
                                            ' since last visit. DO NOT PROVIDE DATE')

    def validate_took_formula(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('took_formula') == YES:
            if not cleaned_data.get('is_first_formula'):
                raise forms.ValidationError(
                    'Infant took formula, is this the first reporting of infant formula use?')
        else:
            if cleaned_data.get('is_first_formula'):
                raise forms.ValidationError('You mentioned that infant did not take formula,'
                                            ' PLEASE DO NOT PROVIDE FIRST FORMULA USE INFO')

        if cleaned_data.get('is_first_formula') == YES:
            if not cleaned_data.get('date_first_formula') and not cleaned_data.get('est_date_first_formula'):
                raise forms.ValidationError('If this is a first reporting of infant formula'
                                            ' please provide date and if date is estimated')
        else:
            if cleaned_data.get('date_first_formula') and cleaned_data.get('est_date_first_formula'):
                raise forms.ValidationError('You mentioned that is not the first reporting of infant formula'
                                            ' PLEASE DO NOT PROVIDE DATE AND EST DATE')

    def validate_cows_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('cow_milk') == YES:
            if cleaned_data.get('cow_milk_yes') == 'N/A':
                raise forms.ValidationError('If infant took cows milk. Answer CANNOT be Not Applicable')
        else:
            if not cleaned_data.get('cow_milk_yes') == 'N/A':
                raise forms.ValidationError('Infant did not take cows milk. Answer is NOT APPLICABLE')

    def validate_formula_intro_occur(self, cleaned_data):
        if cleaned_data.get('formula_intro_occur') == YES:
            if cleaned_data.get('formula_intro_date'):
                answer = False
                for question in ['juice', 'cow_milk', 'other_milk', 'fruits_veg',
                                 'cereal_porridge', 'solid_liquid']:
                    if cleaned_data.get(question) == YES:
                        answer = True
                        break
                if not answer:
                    raise forms.ValidationError(
                        'You should answer YES either on {}, {}, {}, {}, {} or {}.'.format(
                            cleaned_data.get('juice'),
                            cleaned_data.get('cow_milk'),
                            cleaned_data.get('other_milk'),
                            cleaned_data.get('fruits_veg'),
                            cleaned_data.get('cereal_porridge'),
                            cleaned_data.get('solid_liquid')))

    class Meta:
        model = InfantFeeding
        fields = '__all__'
