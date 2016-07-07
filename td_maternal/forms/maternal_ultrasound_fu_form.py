from django import forms

from ..models import MaternalUltraSoundFu
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalUltraSoundFuForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalUltraSoundFuForm, self).clean()
        return cleaned_data

    class Meta:
        model = MaternalUltraSoundFu
        fields = '__all__'
