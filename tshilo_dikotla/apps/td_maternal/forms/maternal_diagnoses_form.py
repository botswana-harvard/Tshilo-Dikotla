from django import forms

from edc_constants.constants import YES, NOT_APPLICABLE

from ..models import MaternalDiagnoses

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalDiagnosesForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalDiagnosesForm, self).clean()
        return cleaned_data

    def validate_has_diagnoses(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('new_diagnoses') not in [YES]:
            if cleaned_data.get(diagnoses) not in [NOT_APPLICABLE]:
                raise forms.ValidationError('No new diagnoses, do not answer question on new diagnoses.')

    def validate_who_dignoses(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('has_who_dx') == YES:
            if not cleaned_data.get('who') or cleaned_data.get('who') in [NOT_APPLICABLE]:
                raise forms.ValidationError('WHO diagnosis is Yes, please give who diagnosis.')
        if cleaned_data.get('has_who_dx') in [NO, NOT_APPLICABLE]:
            if cleaned_data.get('who') not in [NOT_APPLICABLE]:
                raise forms.ValidationError('WHO diagnoses is {}, please do not give WHO Stage III/IV'.format(cleaned_data.get('has_who_dx')))


    class Meta:
        model = MaternalDiagnoses
        fields = '__all__'
