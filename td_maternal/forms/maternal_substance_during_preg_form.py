from django import forms
from edc_constants.constants import YES

from ..models import MaternalSubstanceUseDuringPreg
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalSubstanceUseDuringPregForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalSubstanceUseDuringPregForm, self).clean()
        self.validate_smoked_during_pregnancy()
        self.validate_alcohol_during_pregnancy()
        self.validate_marijuana_during_preg()
        return cleaned_data

    def validate_smoked_during_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('smoked_during_pregnancy') in [YES]:
            if not cleaned_data.get('smoking_during_preg_freq'):
                raise forms.ValidationError('Participant has smoked tobacco during this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('smoking_during_preg_freq'):
                raise forms.ValidationError('Participant has never smoked tobacco during this pregnancy, please do not give a frequency.')

    def validate_alcohol_during_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('alcohol_during_pregnancy') == YES:
            if not cleaned_data.get('alcohol_during_preg_freq'):
                raise forms.ValidationError('Participant has drank alcohol during this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('alcohol_during_preg_freq'):
                raise forms.ValidationError('Participant has never drank alcohol during this pregnancy, please do not give a frequency.')

    def validate_marijuana_during_preg(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('marijuana_during_preg') == YES:
            if not cleaned_data.get('marijuana_during_preg_freq'):
                raise forms.ValidationError('Participant has smoked marijuana during this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('marijuana_during_preg_freq'):
                raise forms.ValidationError('Participant has never smoked marijuana during this pregnancy, please do not give a frequency.')

    class Meta:
        model = MaternalSubstanceUseDuringPreg
        fields = '__all__'
