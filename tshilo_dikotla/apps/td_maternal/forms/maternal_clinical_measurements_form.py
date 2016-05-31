from django import forms

from ..models import MaternalClinicalMeasurementsOne, MaternalClinicalMeasurementsTwo

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalClinicalMeasurementsOneForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalClinicalMeasurementsOneForm, self).clean()
        if cleaned_data.get('systolic_bp') < cleaned_data.get('diastolic_bp'):
            raise forms.ValidationError(
                'Systolic blood pressure cannot be lower than the diastolic blood pressure.'
                ' Please correct.')
        return cleaned_data

    class Meta:
        model = MaternalClinicalMeasurementsOne
        fields = '__all__'


class MaternalClinicalMeasurementsTwoForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalClinicalMeasurementsTwoForm, self).clean()
        if cleaned_data.get('systolic_bp') < cleaned_data.get('diastolic_bp'):
            raise forms.ValidationError(
                'Systolic blood pressure cannot be lower than the diastolic blood pressure.'
                ' Please correct.')
        return cleaned_data

    class Meta:
        model = MaternalClinicalMeasurementsTwo
        fields = '__all__'
