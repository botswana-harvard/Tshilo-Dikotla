from django import forms

from ..models import MaternalAztNvp
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalAztNvpForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalAztNvpForm, self).clean()
        return cleaned_data

    class Meta:
        model = MaternalAztNvp
        fields = '__all__'
