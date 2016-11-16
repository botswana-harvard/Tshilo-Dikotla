from django import forms

from edc_constants.constants import YES, NO
from .base_maternal_model_form import BaseMaternalModelForm
from ..models import NvpDispensing


class NvpDispensingForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(NvpDispensingForm, self).clean()
        self.validate_correct_dose()
        self.validate_week_2_dose()
        return cleaned_data

    def validate_correct_dose(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('correct_dose') == NO:
            if not cleaned_data.get('corrected_dose'):
                raise forms.ValidationError(
                    'If the correct dose was not given, please give the corrected dose.')
        else:
            if cleaned_data.get('corrected_dose'):
                raise forms.ValidationError(
                    'If the correct dose was given, please do not give the corrected dose.')

    def validate_week_2_dose(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('dose_adjustment') == YES:
            if not cleaned_data.get('week_2_dose'):
                raise forms.ValidationError(
                    'If infant came for a week 2 dose adjustment, '
                    'please give the week 2 dose.')
        else:
            if cleaned_data.get('week_2_dose'):
                raise forms.ValidationError(
                    'If infant did not come for a week 2 dose adjustment, '
                    'please do not give the week 2 dose.')

    class Meta:
        model = NvpDispensing
        fields = '__all__'
