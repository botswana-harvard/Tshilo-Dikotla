from django import forms

from edc_constants.constants import OTHER, NO, YES

from ..models import InfantFuNewMed, InfantFuNewMedItems

from .base_infant_model_form import BaseInfantModelForm


class InfantFuNewMedForm(BaseInfantModelForm):

    class Meta:
        model = InfantFuNewMed
        fields = '__all__'


class InfantFuNewMedItemsForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantFuNewMedItemsForm, self).clean()
        self.validate_new_medications()
        self.validate_stop_date()
        self.validate_other()
        return cleaned_data

    def validate_new_medications(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('infant_fu_med').new_medications == YES:
            if not cleaned_data.get('medication'):
                raise forms.ValidationError(
                    'You have indicated that participant took medications. Please provide them.')
        if cleaned_data.get('infant_fu_med').new_medications == NO:
            raise forms.ValidationError('You indicated that no medications were taken. You cannot provide the '
                                        'medication. Please correct')

    def validate_stop_date(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('stop_date'):
            if cleaned_data.get('stop_date') < cleaned_data.get('date_first_medication'):
                raise forms.ValidationError('You have indicated that medication stop date is before its start date. '
                                            'Please correct.')

    def validate_other(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('medication') == OTHER and not cleaned_data.get('other_medication'):
            raise forms.ValidationError('Please specify other medication.')
        if not cleaned_data.get('medication') == OTHER and cleaned_data.get('other_medication'):
            raise forms.ValidationError('Please select Other in Medication '
                                        'in when if Other medication is being record.')

    class Meta:
        model = InfantFuNewMedItems
        fields = '__all__'
