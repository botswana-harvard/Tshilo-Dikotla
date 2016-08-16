from django import forms

from edc_constants.constants import YES, NO, NOT_APPLICABLE

from ..models import MaternalDiagnoses

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalDiagnosesForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalDiagnosesForm, self).clean()
        self.validate_has_diagnoses()
        self.validate_who_dignoses()
        return cleaned_data

    def validate_has_diagnoses(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('new_diagnoses') in [YES]:
            if not cleaned_data.get('diagnoses'):
                raise forms.ValidationError('Participant has new diagnoses, please give a diagnosis.')
            if self.validate_not_applicable_in_there('diagnoses'):
                raise forms.ValidationError('New Diagnoses is Yes, diagnoses list cannot have Not Applicable. Please correct.')
        else:
            if self.validate_not_applicable_not_there('diagnoses') or self.validate_not_applicable_and_other_options('diagnoses'):
                raise forms.ValidationError('Participant does not have any new diagnoses, new diagnosis should be Not Applicable.')

    def validate_who_dignoses(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('has_who_dx') == YES:
            if not cleaned_data.get('who'):
                raise forms.ValidationError('WHO diagnosis is Yes, please give who diagnosis.')
            if self.validate_not_applicable_in_there('who'):
                raise forms.ValidationError('WHO Stage III/IV cannot have Not Applicable in the list. Please correct.')
        if cleaned_data.get('has_who_dx') in [NO, NOT_APPLICABLE]:
            if self.validate_not_applicable_not_there('who'):
                raise forms.ValidationError('WHO diagnoses is {}, WHO Stage III/IV should be Not Applicable.'.format(cleaned_data.get('has_who_dx')))


    class Meta:
        model = MaternalDiagnoses
        fields = '__all__'
