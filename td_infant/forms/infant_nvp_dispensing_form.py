from django import forms

from edc_constants.constants import YES, NO

from ..models import InfantNvpDispensing

from .base_infant_model_form import BaseInfantModelForm


class InfantNvpDispensingForm(BaseInfantModelForm, forms.ModelForm):

    def clean(self):
        cleaned_data = super(InfantNvpDispensingForm, self).clean()
        self.validate_nvp_prohylaxis()
        self.validate_correct_dose()
        return cleaned_data

    def validate_nvp_prohylaxis(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('nvp_prophylaxis') == YES:
            if not cleaned_data.get('azt_prophylaxis'):
                raise forms.ValidationError(
                    'Was the infant given AZT infant prophylaxis? Please answer YES or NO')
            if cleaned_data.get('reason_not_given'):
                raise forms.ValidationError(
                    'Infant received NVP prophylaxis, do not give reason.')
            if not cleaned_data.get('nvp_admin_date'):
                raise forms.ValidationError(
                    'Please give the NVP infant prophylaxis date.')
            if not cleaned_data.get('medication_instructions'):
                raise forms.ValidationError(
                    'If the Infant received NVP prophylaxis, was the mother '
                    'given instructions on how to administer the medication?')
            if not cleaned_data.get('dose_admin_infant'):
                raise forms.ValidationError(
                    'Please give the NVP prophylaxis dosage information.')
            if not cleaned_data.get('correct_dose'):
                raise forms.ValidationError(
                    'Was the correct NVP prophylaxis dose given?')
        else:
            if not cleaned_data.get('reason_not_given'):
                raise forms.ValidationError(
                    'Infant did NOT receive NVP infant prophylaxis, please give a reason.')

    def validate_azt_prophylaxis(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('azt_prophylaxis') == YES:
            if not cleaned_data.get('azt_dose_given'):
                raise forms.ValidationError(
                    'Infant received AZT prophylaxis, please give the dose administered.')
        else:
            if cleaned_data.get('azt_dose_given'):
                raise forms.ValidationError(
                    'Infant did NOT receive AZT prophylaxis, please do not give the dose.')

    class Meta:
        model = InfantNvpDispensing
        fields = '__all__'
