from django import forms

from edc_constants.constants import NO, YES

from ..models import InfantFuDx, InfantFuDxItems

from .base_infant_model_form import BaseInfantModelForm


class InfantFuDxForm(BaseInfantModelForm):

    class Meta:
        model = InfantFuDx
        fields = '__all__'


class InfantFuDxItemsForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantFuDxItemsForm, self).clean()
        if cleaned_data.get('health_facility') == NO:
            if cleaned_data.get('was_hospitalized') == YES:
                raise forms.ValidationError(
                    'You indicated that participant was hospitalized, therefore the participant '
                    'was seen at a health facility. Please correct.')
        return cleaned_data

    class Meta:
        model = InfantFuDxItems
        fields = '__all__'
