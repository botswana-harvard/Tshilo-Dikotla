from django import forms

from ..models import MaternalInterimIdcc
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalInterimIdccForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalInterimIdccForm, self).clean()
        return cleaned_data

    class Meta:
        model = MaternalInterimIdcc
        fields = '__all__'
