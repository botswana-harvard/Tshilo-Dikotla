from django import forms

from edc_constants.constants import YES

from .base_infant_model_form import BaseInfantModelForm

from ..models import InfantNvpAdjustment


class InfantNvpAdjustmentForm(BaseInfantModelForm, forms.ModelForm):

    def clean(self):
        cleaned_data = super(InfantNvpAdjustmentForm, self).clean()
        self.validate_dose_adjustment()
        self.validate_dose_4_weeks()
        return cleaned_data

    def validate_dose_adjustment(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('dose_adjustment') == YES:
            if not cleaned_data.get('adjusted_dose'):
                raise forms.ValidationError(
                    'If there was a dose adjustment, please give the adjusted dose.')
        else:
            if cleaned_data.get('adjusted_dose'):
                raise forms.ValidationError(
                    'Infant\'s dose was not adjusted, please do not give an adjust dose.')

    def validate_dose_4_weeks(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('dose_4_weeks') == YES:
            if cleaned_data.get('incomplete_dose'):
                raise forms.ValidationError(
                    'Medication was taken daily for 4 weeks, don\'t give reason for incomplete dose.')
        else:
            if not cleaned_data.get('incomplete_dose'):
                raise forms.ValidationError(
                    'Medication was not taken daily for 4 weeks, please give reason for incomplete.')

    class Meta:
        model = InfantNvpAdjustment
        fields = '__all__'
