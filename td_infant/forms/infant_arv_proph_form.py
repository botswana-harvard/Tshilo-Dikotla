from django import forms
from django.forms.models import ModelForm

from edc_constants.constants import NO, YES, NOT_APPLICABLE, UNKNOWN

from tshilo_dikotla.constants import MODIFIED, DISCONTINUED, NEVER_STARTED

from ..models import InfantArvProph, InfantArvProphMod, InfantVisit, InfantBirthArv

from .base_infant_model_form import BaseInfantModelForm


def get_birth_arv_visit_2000(infant_identifier):
    """Check if infant was given AZT at birth"""
    try:
        visit_2000 = InfantVisit.objects.get(
            subject_identifier=infant_identifier, appointment__visit_definition__code=2000)
        infant_birth_arv = InfantBirthArv.objects.get(infant_visit=visit_2000)
        return infant_birth_arv.azt_discharge_supply
    except Exception as e:
        pass
    return NOT_APPLICABLE


class InfantArvProphForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        # self.validate_taking_arv_proph_no()
        self.validate_taking_arv_proph_unknown()
        self.validate_taking_arv_proph_yes()
        return cleaned_data

    def validate_taking_arv_proph_no(self):
        cleaned_data = self.cleaned_data
        infant_identifier = cleaned_data.get('infant_visit').subject_identifier
        if cleaned_data.get('prophylatic_nvp') == NO:
            if cleaned_data.get('arv_status') not in [NEVER_STARTED, DISCONTINUED]:
                raise forms.ValidationError(
                    'Infant was not taking prophylactic arv, prophylaxis should be Never Started or Discontinued.')
            if (cleaned_data.get('arv_status') == DISCONTINUED and
                    get_birth_arv_visit_2000(infant_identifier)) in [NO, UNKNOWN]:
                raise forms.ValidationError(
                    'The azt discharge supply in Infant birth arv was answered as NO or Unknown, '
                    'therefore Infant ARV proph in this visit cannot be permanently discontinued.')

    def validate_taking_arv_proph_unknown(self):
        cleaned_data = self.cleaned_data
        infant_identifier = cleaned_data.get('infant_visit').subject_identifier
        if cleaned_data.get('prophylatic_nvp') == UNKNOWN and cleaned_data.get('arv_status') not in ['modified']:
            if get_birth_arv_visit_2000(infant_identifier) not in [UNKNOWN]:
                raise forms.ValidationError(
                    'The azt discharge supply in Infant Birth arv was not answered as UNKNOWN, Q3 cannot be Unknown.')

    def validate_taking_arv_proph_yes(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('prophylatic_nvp') == YES and
                cleaned_data.get('arv_status') in [NEVER_STARTED, DISCONTINUED]):
            raise forms.ValidationError(
                'Infant has been on prophylactic arv, cannot choose Never Started or Permanently discontinued.')

    class Meta:
        model = InfantArvProph
        fields = '__all__'


class InfantArvProphModForm(ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_proph_mod_fields()
        self.validate_infant_arv_proph_not_modified()
        self.validate_infant_arv_code()
        return cleaned_data

    def validate_proph_mod_fields(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('arv_code'):
            if not cleaned_data.get('dose_status'):
                raise forms.ValidationError(
                    'You entered an ARV Code, please give the dose status.')

            if not cleaned_data.get('modification_date'):
                raise forms.ValidationError(
                    'You entered an ARV Code, please give the modification date.')

            if not cleaned_data.get('modification_code'):
                raise forms.ValidationError(
                    'You entered an ARV Code, please give the modification reason.')

    def validate_infant_arv_proph_not_modified(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('infant_arv_proph').arv_status != MODIFIED:
            raise forms.ValidationError("You did NOT indicate that medication was modified, so do not ENTER "
                                        "arv inline.")

    def validate_infant_arv_proph_modified(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('infant_arv_proph').arv_status == MODIFIED:
            raise forms.ValidationError("You indicated that medication was never modified, so ENTER "
                                        "arv inline.")

    def validate_infant_arv_proph_never_started(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('infant_arv_proph').arv_status == NEVER_STARTED:
            raise forms.ValidationError("You indicated that medication was never started, so do not ENTER "
                                        "arv inline.")

    def validate_infant_arv_code(self):
        cleaned_data = self.cleaned_data
        infant_identifier = cleaned_data.get(
            'infant_arv_proph').infant_visit.subject_identifier
        if (cleaned_data.get('arv_code') == 'Zidovudine' and
                get_birth_arv_visit_2000(infant_identifier) in [YES]):
            if cleaned_data.get('modification_code') in ['Initial dose']:
                raise forms.ValidationError(
                    'Infant birth ARV shows that infant was discharged with an additional dose of AZT, '
                    'AZT cannot be initiated again.')
        if get_birth_arv_visit_2000(infant_identifier) in [YES] and cleaned_data.get('arv_code') not in ['Zidovudine']:
            raise forms.ValidationError(
                'Infant birth ARV shows that infant was discharged with an additional dose of AZT, '
                'Arv Code should be AZT')

    class Meta:
        model = InfantArvProphMod
        fields = '__all__'
