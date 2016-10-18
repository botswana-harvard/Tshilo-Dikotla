from django import forms
from edc_constants.constants import YES

from ..models import MaternalSubstanceUsePriorPreg
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalSubstanceUsePriorPregForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalSubstanceUsePriorPregForm, self).clean()
        self.validate_smoked_prior_pregnancy()
        self.validate_alcohol_prior_pregnancy()
        self.validate_marijuana_prior_preg()
        return cleaned_data

    def validate_smoked_prior_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('smoked_prior_to_preg') in [YES]:
            if not cleaned_data.get('smoking_prior_preg_freq'):
                raise forms.ValidationError(
                    'Participant has smoked tobacco prior to this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('smoking_prior_preg_freq'):
                raise forms.ValidationError(
                    'Participant has never smoked tobacco prior to this pregnancy, please do not give a frequency.')

    def validate_alcohol_prior_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('alcohol_prior_pregnancy') == YES:
            if not cleaned_data.get('alcohol_prior_preg_freq'):
                raise forms.ValidationError('Participant has drank alcohol prior this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('alcohol_prior_preg_freq'):
                raise forms.ValidationError('Participant has never drank alcohol prior this pregnancy, please do not give a frequency.')

    def validate_marijuana_prior_preg(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('marijuana_prior_preg') == YES:
            if not cleaned_data.get('marijuana_prior_preg_freq'):
                raise forms.ValidationError('Participant has smoked marijuana prior to this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('marijuana_prior_preg_freq'):
                raise forms.ValidationError('Participant has never smoked marijuana prior to this pregnancy, please do not give a frequency.')

    class Meta:
        model = MaternalSubstanceUsePriorPreg
        fields = '__all__'
