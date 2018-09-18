from django import forms

from ..models import MaternalPostPartumDep
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalPostPartumDepForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalPostPartumDepForm, self).clean()
        return cleaned_data

    total_score = forms.CharField(
        label='Total score',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = MaternalPostPartumDep
        fields = '__all__'
