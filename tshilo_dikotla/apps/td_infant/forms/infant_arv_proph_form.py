from django import forms
from django.forms.models import ModelForm

from edc_constants.constants import NO, YES

from tshilo_dikotla.apps.td.constants import MODIFIED, DISCONTINUED, NEVER_STARTED

from ..models import InfantArvProph, InfantArvProphMod

from .base_infant_model_form import BaseInfantModelForm


class InfantArvProphForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_taking_arv_proph_no()
        self.validate_taking_arv_proph_yes()
        return cleaned_data

    def validate_taking_arv_proph_no(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('prophylatic_nvp') == NO and
                (cleaned_data.get('arv_status') != NEVER_STARTED or cleaned_data.get('arv_status') != DISCONTINUED)):
            raise forms.ValidationError('Infant was not taking prophylactic arv, prophylaxis should be Never Started.')

    def validate_taking_arv_proph_yes(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('prophylatic_nvp') == YES and cleaned_data.get('arv_status') == NEVER_STARTED:
            raise forms.ValidationError('Infant has been on prophylactic arv, cannot choose Never Started.')

    class Meta:
        model = InfantArvProph
        fields = '__all__'


class InfantArvProphModForm(ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_proph_mod_fields()
        self.validate_infant_arv_proph_not_modified()
        return cleaned_data

    def validate_proph_mod_fields(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('arv_code'):
            if not cleaned_data.get('dose_status'):
                raise forms.ValidationError('You entered an ARV Code, please give the dose status.')

            if not cleaned_data.get('modification_date'):
                raise forms.ValidationError('You entered an ARV Code, please give the modification date.')

            if not cleaned_data.get('modification_code'):
                raise forms.ValidationError('You entered an ARV Code, please give the modification reason.')

    def validate_infant_arv_proph_not_modified(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('infant_arv_proph').arv_status != MODIFIED:
            raise forms.ValidationError("You did NOT indicate that medication was modified, so do not ENTER "
                                        "arv inline.")

    class Meta:
        model = InfantArvProphMod
        fields = '__all__'
