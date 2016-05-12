from django import forms

from ..models import MaternalUltraSoundInitial
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalUltraSoundInitialForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalUltraSoundInitialForm, self).clean()
        return cleaned_data

    class Meta:
        model = MaternalUltraSoundInitial
        fields = '__all__'
