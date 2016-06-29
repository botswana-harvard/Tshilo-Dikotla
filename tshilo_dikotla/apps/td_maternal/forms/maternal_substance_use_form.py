from django import forms
from edc_constants.constants import YES

from ..models import MaternalSubstanceUse
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalSubstanceUseForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalSubstanceUseForm, self).clean()
        self.validate_smoked_prior_pregnancy()
        self.validate_smoked_during_pregnancy()
        self.validate_alcohol_during_pregnancy()
        self.validate_marijuana_prior_preg()
        self.validate_marijuana_during_preg()
        return cleaned_data

    def validate_smoked_prior_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('smoked_prior_to_preg') in [YES]:
            if not cleaned_data.get('smoking_prior_preg_freq'):
                raise forms.ValidationError('Participant has smoked tobacco prior to this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('smoking_prior_preg_freq'):
                raise forms.ValidationError('Participant has never smoked tobacco prior to this pregnancy, please do not give a frequency.')

    def validate_smoked_during_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('smoked_during_to_preg') == YES:
            if not cleaned_data.get('smoking_during_preg_freq'):
                raise forms.ValidationError('Participant has smoked tobacco during to this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('smoking_during_preg_freq'):
                raise forms.ValidationError('Participant has never smoked tobacco during to this pregnancy, please do not give a frequency.')

    def validate_alcohol_during_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('alcohol_during_pregnancy') == YES:
            if not cleaned_data.get('alcohol_during_preg_freq'):
                raise forms.ValidationError('Participant has drank alcohol during this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('alcohol_during_preg_freq'):
                raise forms.ValidationError('Participant has never drank alcohol during this pregnancy, please do not give a frequency.')

    def validate_marijuana_prior_preg(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('marijuana_prior_preg') == YES:
            if not cleaned_data.get('marijuana_prior_preg_freq'):
                raise forms.ValidationError('Participant has smoked marijuana prior to this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('marijuana_prior_preg_freq'):
                raise forms.ValidationError('Participant has never smoked marijuana prior to this pregnancy, please do not give a frequency.')

    def validate_marijuana_during_preg(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('marijuana_during_preg') == YES:
            if not cleaned_data.get('marijuana_during_preg_freq'):
                raise forms.ValidationError('Participant has smoked marijuana during to this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('marijuana_during_preg_freq'):
                raise forms.ValidationError('Participant has never smoked marijuana during to this pregnancy, please do not give a frequency.')

    class Meta:
        model = MaternalSubstanceUse
        fields = '__all__'
