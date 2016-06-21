from django import forms
from edc_constants.constants import YES

from ..models import InfantFu
from .base_infant_model_form import BaseInfantModelForm


class InfantFuForm(BaseInfantModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data

        if cleaned_data.get('was_hospitalized') == YES:
            if not cleaned_data.get('days_hospitalized'):
                raise forms.ValidationError('If infant was hospitalized, please provide # of days hospitalized')
            if cleaned_data.get('days_hospitalized') > 90:
                raise forms.ValidationError('days hospitalized cannot be greater than 90days')
        return super(InfantFuForm, self).clean()

    class Meta:
        model = InfantFu
        fields = '__all__'
