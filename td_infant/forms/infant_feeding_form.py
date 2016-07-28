from django import forms

from edc_constants.constants import YES, NO, NOT_APPLICABLE

from .base_infant_model_form import BaseInfantModelForm
from ..models import InfantFeeding


class InfantFeedingForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantFeedingForm, self).clean()
        self.validate_other_feeding()
        self.validate_took_formula()
        self.validate_took_formula_not_yes()
        self.validate_cows_milk()
        self.validate_took_other_milk()
        self.validate_breast_milk_weaning()
        self.validate_formula_intro_occur(cleaned_data)
        return cleaned_data

    def validate_other_feeding(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('formula_intro_occur') == YES:
            if not cleaned_data.get('formula_intro_date'):
                raise forms.ValidationError('Question3: If received formula milk | foods | liquids since last'
                                            ' attended visit. Please provide intro date')
        else:
            if cleaned_data.get('formula_intro_date'):
                raise forms.ValidationError('You mentioned no formula milk | foods | liquids received'
                                            ' since last visit in question 3. DO NOT PROVIDE DATE')

    def validate_took_formula(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('took_formula') == YES:
            if not cleaned_data.get('is_first_formula'):
                raise forms.ValidationError(
                    'Question7: Infant took formula, is this the first reporting of infant formula use?'
                    ' Please provide YES or NO')

            if cleaned_data.get('is_first_formula') == YES:
                if not cleaned_data.get('date_first_formula'):
                    raise forms.ValidationError('If this is a first reporting of infant formula'
                                                ' please provide date and if date is estimated')

                if not cleaned_data.get('est_date_first_formula'):
                    raise forms.ValidationError('If this is a first reporting of infant formula'
                                                ' please provide date and if date is estimated')
            if cleaned_data.get('is_first_formula') == NO:
                if cleaned_data.get('date_first_formula'):
                    raise forms.ValidationError('Question8: You mentioned that is not the first reporting of infant'
                                                ' formula PLEASE DO NOT PROVIDE DATE')
                if cleaned_data.get('est_date_first_formula'):
                    raise forms.ValidationError('Question9: You mentioned that is not the first reporting of infant'
                                                ' formula PLEASE DO NOT PROVIDE EST DATE')

    def validate_took_formula_not_yes(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('took_formula') != YES:
            if cleaned_data.get('is_first_formula'):
                raise forms.ValidationError('Question7: You mentioned that infant did not take formula,'
                                            ' PLEASE DO NOT PROVIDE FIRST FORMULA USE INFO')

            if cleaned_data.get('date_first_formula'):
                raise forms.ValidationError('Question8: You mentioned that infant did not take formula,'
                                            ' PLEASE DO NOT PROVIDE DATE OF FIRST FORMULA USE')

            if cleaned_data.get('est_date_first_formula'):
                raise forms.ValidationError('Question9: You mentioned that infant did not take formula,'
                                            ' PLEASE DO NOT PROVIDE ESTIMATED DATE OF FIRST FORMULA USE')

    def validate_cows_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('cow_milk') == YES:
            if cleaned_data.get('cow_milk_yes') == 'N/A':
                raise forms.ValidationError('Question13: If infant took cows milk. Answer CANNOT be Not Applicable')
        else:
            if not cleaned_data.get('cow_milk_yes') == 'N/A':
                raise forms.ValidationError('Question13: Infant did not take cows milk. Answer is NOT APPLICABLE')

    def validate_took_other_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('other_milk') == YES:
            if not cleaned_data.get('other_milk_animal'):
                raise forms.ValidationError('Question15: The infant took milk from another animal, please specify'
                                            ' which?')
            if cleaned_data.get('milk_boiled') == NOT_APPLICABLE:
                raise forms.ValidationError('Question16:The infant took milk from another animal, answer'
                                            ' cannot be N/A')
        else:
            if cleaned_data.get('other_milk_animal'):
                raise forms.ValidationError('Question15: The infant did not take milk from any other animal, please'
                                            ' do not provide the name of the animal')

            if cleaned_data.get('milk_boiled') != NOT_APPLICABLE:
                raise forms.ValidationError('Question16: The infant did not take milk from any other animal, the'
                                            ' answer for whether the milk was boiled should be N/A')

    def validate_breast_milk_weaning(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('ever_breastfeed') == YES:
            if cleaned_data.get('complete_weaning') != NOT_APPLICABLE:
                raise forms.ValidationError('Question24: The infant has been breastfed since the last visit, The answer'
                                            ' answer should be N/A')
        else:
            if cleaned_data.get('complete_weaning') == NOT_APPLICABLE:
                raise forms.ValidationError('Question24: The infant has not been breastfed since the last visit, '
                                            'The answer should not be N/A')

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
                        'You should answer YES on either one of the questions about the juice, cow_milk, other milk, '
                        'fruits_veg, cereal_porridge or solid_liquid')

    class Meta:
        model = InfantFeeding
        fields = '__all__'
