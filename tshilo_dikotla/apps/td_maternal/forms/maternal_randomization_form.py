from django import forms

from ..models import MaternalRando
from ..classes import Randomization
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalRandomizationForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalRandomizationForm, self).clean()
        randomization_helper = Randomization(MaternalRando(**cleaned_data),
                                             error_clss=forms.ValidationError)
        randomization_helper.verify_hiv_status()
        return cleaned_data

    class Meta:
        model = MaternalRando
        fields = '__all__'
