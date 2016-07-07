from django import forms
from django.forms import ModelForm

from edc_constants.constants import YES, NO

from ..models import MaternalEligibility


class MaternalEligibilityForm(ModelForm):

    def clean(self):
        return super(MaternalEligibilityForm, self).clean()

    class Meta:
        model = MaternalEligibility
        fields = '__all__'
