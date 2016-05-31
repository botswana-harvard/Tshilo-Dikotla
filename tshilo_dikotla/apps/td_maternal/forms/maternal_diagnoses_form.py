from django import forms

from ..models import MaternalDiagnoses

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalDiagnosesForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalDiagnosesForm, self).clean()
        return cleaned_data

    class Meta:
        model = MaternalDiagnoses
        fields = '__all__'
