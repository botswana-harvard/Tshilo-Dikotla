from django import forms
from django.forms.models import ModelForm

from edc_constants.constants import NO, YES, NOT_APPLICABLE, UNKNOWN

from tshilo_dikotla.constants import MODIFIED, DISCONTINUED, NEVER_STARTED, START

from ..models import InfantArvProph, InfantArvProphMod, InfantVisit, InfantBirthArv

from .base_infant_model_form import BaseInfantModelForm


def get_birth_arv_visit_2000(infant_identifier):
    """Check if infant was given AZT at birth"""
    try:
        visit_2000 = InfantVisit.objects.get(
            subject_identifier=infant_identifier, appointment__visit_definition__code=2000, appointment__visit_instance=0)
        infant_birth_arv = InfantBirthArv.objects.get(infant_visit=visit_2000)
        return infant_birth_arv.azt_discharge_supply
    except InfantBirthArv.DoesNotExist:
        pass
    return NOT_APPLICABLE


class InfantArvProphForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_taking_arv_proph_no()
        self.validate_taking_arv_proph_unknown()
        self.validate_taking_arv_proph_yes()
        return cleaned_data

    def validate_taking_arv_proph_no(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('prophylatic_nvp') == NO:
            raise forms.ValidationError(
                {'prophylatic_nvp': 'Infant is HEU, answer cannot be No.'})

    def validate_taking_arv_proph_unknown(self):
        cleaned_data = self.cleaned_data
        infant_identifier = cleaned_data.get('infant_visit').subject_identifier
        if cleaned_data.get('prophylatic_nvp') == UNKNOWN and cleaned_data.get('arv_status') not in ['modified']:
            if get_birth_arv_visit_2000(infant_identifier) not in [UNKNOWN]:
                raise forms.ValidationError(
                    'The azt discharge supply in Infant Birth arv was not answered as UNKNOWN, Q3 cannot be Unknown.')

    def validate_taking_arv_proph_yes(self):
        cleaned_data = self.cleaned_data
        arv_proph_mod = self.data.get(
            'infantarvprophmod_set-0-arv_code')
        if cleaned_data.get('prophylatic_nvp') == YES:
            if cleaned_data.get('arv_status') in [START, MODIFIED] and not arv_proph_mod:
                raise forms.ValidationError(
                    {'arv_status': 'Please complete the infant arv proph mods table.'})
            if cleaned_data.get('arv_status') == NEVER_STARTED and arv_proph_mod:
                raise forms.ValidationError(
                    {'arv_status': 'Infant never started prophlaxis, do not complete '
                     'the infant arv proph mods table.'})

    class Meta:
        model = InfantArvProph
        fields = '__all__'


class InfantArvProphModForm(ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_proph_mod_fields()
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
