from django import forms

from ..models import MaternalUltraSoundInitial
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalUltraSoundInitialForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalUltraSoundInitialForm, self).clean()
        MaternalUltraSoundInitial(**cleaned_data).evaluate_edd_confirmed(error_clss=forms.ValidationError)
        return cleaned_data

    class Meta:
        model = MaternalUltraSoundInitial
        fields = '__all__'
