from django import forms

from ..models import InfantBirthArv

from edc_constants.constants import YES

from .base_infant_model_form import BaseInfantModelForm


class InfantBirthArvForm(BaseInfantModelForm):

    class Meta:
        model = InfantBirthArv
        fields = '__all__'

    def clean(self):
        cleaned_data = super(InfantBirthArvForm, self).clean()
        self.validate_azt_after_birth()
        self.validate_sdnvp_after_birth()
        return cleaned_data

    def validate_azt_after_birth(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('azt_after_birth') == YES:
            if not cleaned_data.get('azt_dose_date'):
                raise forms.ValidationError('Provide date of the first dose for AZT.')
            if cleaned_data.get('azt_additional_dose') == 'N/A':
                raise forms.ValidationError('Do not select Not applicable for Q6 if Q4 answer was yes.')
        else:
            if cleaned_data.get('azt_dose_date'):
                raise forms.ValidationError('Participant indicated that AZT was NOT provided. '
                                            'You cannot provide date of first dose')

    def validate_sdnvp_after_birth(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('sdnvp_after_birth') == YES:
            if not cleaned_data.get('nvp_dose_date'):
                raise forms.ValidationError('If infant has received single dose NVP then provide NVP date.')
        else:
            if cleaned_data.get('nvp_dose_date'):
                raise forms.ValidationError('Participant indicated that NVP was NOT provided. '
                                            'You cannot provide date of first dose.')
