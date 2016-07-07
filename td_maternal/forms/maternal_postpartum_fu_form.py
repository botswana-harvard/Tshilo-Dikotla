from django import forms

from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS, NEG

from td_maternal.classes import MaternalStatusHelper
from td_list.models import MaternalDiagnoses

from ..models import MaternalPostPartumFu
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalPostPartumFuForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalPostPartumFuForm, self).clean()
        self.validate_has_diagnoses()
#         self.validate_hospitalized_yes()
#         self.validate_hospitalized_no()
#         self.validate_who_dignoses()
        return cleaned_data

    def validate_has_diagnoses(self):

        cleaned_data = self.cleaned_data
        if not cleaned_data.get('diagnoses'):
                raise forms.ValidationError('Question4: Diagnosis field should not be left empty')

        diagnoses_qs = cleaned_data.get('diagnoses').values_list('short_name', flat=True)
        diagnoses_list = list(diagnoses_qs.all())
        if cleaned_data.get('new_diagnoses') == NO:
            if NOT_APPLICABLE not in diagnoses_list:
                raise forms.ValidationError(
                    'Question4: Participant has no new diagnoses, do not give a listing, rather give N/A')
            if NOT_APPLICABLE in diagnoses_list and len(diagnoses_list) > 1:
                raise forms.ValidationError(
                    'Question4: Participant has no new diagnoses, do not give a listing, only give N/A')
        if cleaned_data.get('new_diagnoses') == YES:
            if NOT_APPLICABLE in diagnoses_list:
                raise forms.ValidationError(
                    'Question4: Participant has new diagnoses, list of diagnosis cannot be N/A')

#     def validate_hospitalized_yes(self):
#         cleaned_data = self.cleaned_data
#         if cleaned_data.get('hospitalized') == YES:
#             if not cleaned_data.get('hospitalization_reason'):
#                 raise forms.ValidationError(
#                     'Question7: Patient was hospitalized, please give hospitalization_reason.')
#             if cleaned_data.get('hospitalization_reason') != 'Other':
#                 if cleaned_data.get('hospitalization_other'):
#                     raise forms.ValidationError(
#                         'Question8: Although the mother was hospitalized, other was not selected so do not give other reason')
#             if not cleaned_data.get('hospitalization_days'):
#                 raise forms.ValidationError(
#                     'Question9: The mother was hospitalized, please give the hospitalization days')
# 
#     def validate_hospitalized_no(self):
#         cleaned_data = self.cleaned_data
#         if cleaned_data.get('hospitalized') == NO:
#             if cleaned_data.get('hospitalization_reason'):
#                 raise forms.ValidationError(
#                     'Question7: Patient was not hospitalized, please do not give hospitalization_reason.')
#             if cleaned_data.get('hospitalization_other'):
#                 raise forms.ValidationError(
#                     'Question8: Patient was not hospitalized, please do not give hospitalization reason.')
#             if cleaned_data.get('hospitalization_days'):
#                 raise forms.ValidationError(
#                     'Question9: Patient was not hospitalized, please do not give hospitalization days')
#  
#     def validate_who_dignoses(self):
#         cleaned_data = self.cleaned_data
#         status_helper = MaternalStatusHelper(cleaned_data.get('maternal_visit'))
#         subject_status = status_helper.hiv_status
# 
#         if subject_status == NEG:
#             if cleaned_data.get('has_who_dx') != NOT_APPLICABLE:
#                 raise forms.ValidationError('The mother is Negative, question 10 for WHO Stage III/IV should be N/A')
# 
#             if cleaned_data.get('who')[0].short_name not in [NOT_APPLICABLE]:
#                 raise forms.ValidationError('The mother is Negative, question 11 for WHO Stage III/IV listing should be N/A')
# 
#         if subject_status == POS:
#             if cleaned_data.get('has_who_dx') == NOT_APPLICABLE:
#                 raise forms.ValidationError(
#                     'The mother is positive, question 10 for WHO Stage III/IV should not be N/A')
#             if cleaned_data.get('has_who_dx') == YES:
#                 if not cleaned_data.get('who') or cleaned_data.get('who')[0].short_name in [NOT_APPLICABLE]:
#                     raise forms.ValidationError('WHO diagnosis is Yes, please give who diagnosis listing.')
#             if cleaned_data.get('has_who_dx') == NO:
#                 if cleaned_data.get('who')[0].short_name != NOT_APPLICABLE:
#                     raise forms.ValidationError(
#                         'The mother has no new WHO Stage III/IV diagnosis, please do not give a listing, rather select N/A')

    class Meta:
        model = MaternalPostPartumFu
        fields = '__all__'
