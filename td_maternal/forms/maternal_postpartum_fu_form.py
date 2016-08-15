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
        self.validate_hospitalized_yes()
        self.validate_hospitalized_no()
        self.validate_who_dignoses_neg()
        self.validate_who_dignoses_pos()
        return cleaned_data

    def validate_has_diagnoses(self):

        cleaned_data = self.cleaned_data
        if self.validate_many_to_many_not_blank('diagnoses'):
                raise forms.ValidationError('Question4: Diagnosis field should not be left empty')

        if cleaned_data.get('new_diagnoses') == NO:
            if self.validate_not_applicable_not_there('diagnoses'):
                raise forms.ValidationError(
                    'Question4: Participant has no new diagnoses, do not give a listing, rather give N/A')
            if self.validate_not_applicable_and_other_options('diagnoses'):
                raise forms.ValidationError(
                    'Question4: Participant has no new diagnoses, do not give a listing, only give N/A')
        if cleaned_data.get('new_diagnoses') == YES:
            if self.validate_not_applicable_in_there('diagnoses'):
                raise forms.ValidationError(
                    'Question4: Participant has new diagnoses, list of diagnosis cannot be N/A')

    def validate_hospitalized_yes(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('hospitalized') == YES:
            if self.validate_many_to_many_not_blank('hospitalization_reason'):
                raise forms.ValidationError(
                    'Question7: Patient was hospitalized, please give hospitalization_reason.')

            if self.validate_not_applicable_in_there('hospitalization_reason'):
                raise forms.ValidationError(
                    'Question7: Participant was hospitalized, reasons cannot be N/A')

            if not cleaned_data.get('hospitalization_days'):
                raise forms.ValidationError(
                    'Question9: The mother was hospitalized, please give number of days hospitalized')

    def validate_hospitalized_no(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('hospitalized') == NO:
            if self.validate_not_applicable_not_there('hospitalization_reason'):
                raise forms.ValidationError(
                    'Question7: Participant was not hospitalized, reason should be N/A')

            if self.validate_not_applicable_and_other_options('hospitalization_reason'):
                raise forms.ValidationError(
                    'Question7: Participant was not hospitalized, reason should only be N/A')

            if cleaned_data.get('hospitalization_other'):
                raise forms.ValidationError(
                    'Question8: Patient was not hospitalized, please do not give hospitalization reason.')
            if cleaned_data.get('hospitalization_days'):
                raise forms.ValidationError(
                    'Question9: Patient was not hospitalized, please do not give hospitalization days')

    def validate_who_dignoses_neg(self):
        cleaned_data = self.cleaned_data
        status_helper = MaternalStatusHelper(cleaned_data.get('maternal_visit'))
        subject_status = status_helper.hiv_status

        if subject_status == NEG:
            if cleaned_data.get('has_who_dx') != NOT_APPLICABLE:
                raise forms.ValidationError('The mother is Negative, question 10 for WHO Stage III/IV should be N/A')

            if self.validate_many_to_many_not_blank('who'):
                raise forms.ValidationError('Question11: Participant is HIV {}, WHO Diagnosis field should be N/A'.format(status_helper.hiv_status))
            
            if self.validate_not_applicable_not_there('who'):
                raise forms.ValidationError(
                    'The mother is Negative, question 11 for WHO Stage III/IV listing should be N/A')

            if self.validate_not_applicable_and_other_options('who'):
                raise forms.ValidationError(
                    'The mother is Negative, question 11 for WHO Stage III/IV listing should only be N/A')

    def validate_who_dignoses_pos(self):
        cleaned_data = self.cleaned_data
        status_helper = MaternalStatusHelper(cleaned_data.get('maternal_visit'))
        subject_status = status_helper.hiv_status

        if subject_status == POS:
            if cleaned_data.get('has_who_dx') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'The mother is positive, question 10 for WHO Stage III/IV should not be N/A')

            if self.validate_many_to_many_not_blank('who'):
                raise forms.ValidationError('Question11: WHO Diagnosis field should not be left empty')

            if cleaned_data.get('has_who_dx') == YES:
                if self.validate_not_applicable_in_there('who'):
                    raise forms.ValidationError(
                        'Question 10 is indicated as YES, who listing cannot be N/A')

            if cleaned_data.get('has_who_dx') == NO:
                if self.validate_not_applicable_not_there('who'):
                    raise forms.ValidationError(
                        'Question 10 is indicated as NO, who listing should be N/A')
                if self.validate_not_applicable_and_other_options('who'):
                    raise forms.ValidationError(
                        'Question 10 is indicated as NO, who listing should only be N/A')


    class Meta:
        model = MaternalPostPartumFu
        fields = '__all__'
