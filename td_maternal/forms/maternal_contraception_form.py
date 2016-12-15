from django import forms

from edc_constants.constants import YES, NO

from ..models import MaternalContraception
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalContraceptionForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalContraceptionForm, self).clean()
        self.validate_more_children()
        self.validate_next_child()
        self.validate_uses_contraceptive()
        self.validate_another_pregnancy()
        self.validate_pap_smear()
        self.validate_pap_smear_result()
        return cleaned_data

    def validate_more_children(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get('more_children') == YES:
            if cleaned_data.get('next_child'):
                raise forms.ValidationError(
                    'You said the client does not desire more children please do not answer '
                    'When would you like to have your next child?')

    def validate_next_child(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('more_children') == YES:
            if not cleaned_data.get('next_child'):
                raise forms.ValidationError('Participant desires more children, question on next child cannot be None.')

    def validate_uses_contraceptive(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('uses_contraceptive') == YES:
            if not cleaned_data.get('contr'):
                raise forms.ValidationError('Participant uses a contraceptive method, please select a valid method')
            if not cleaned_data.get('contraceptive_startdate'):
                raise forms.ValidationError('Participant uses a contraceptive method, please give a contraceptive startdate.')
        else:
            if self.validate_not_applicable_not_there('contr'):
                raise forms.ValidationError(
                    'Participant does not use a contraceptive method, no need to give a contraceptive method')
            if cleaned_data.get('contraceptive_startdate'):
                raise forms.ValidationError('Participant does not use a contraceptive method, no need to give a contraceptive startdate.')

    def validate_another_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('another_pregnancy') == YES:
            if not cleaned_data.get('pregnancy_date'):
                raise forms.ValidationError('Participant is pregnant, please give date participant found out.')
        else:
            if cleaned_data.get('pregnancy_date'):
                raise forms.ValidationError('Participant is not pregnant, do not give a date.')

    def validate_pap_smear(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('pap_smear') == YES:
            if not cleaned_data.get('pap_smear_date'):
                raise forms.ValidationError('Please give the date the pap smear was done.')
            if cleaned_data.get('pap_smear_date'):
                if not cleaned_data.get('pap_smear_estimate'):
                    raise forms.ValidationError(
                        'Pap smear date has been provided, please let us know if this date has been estimated.')
        elif cleaned_data.get('pap_smear') == NO:
            if cleaned_data.get('pap_smear_date'):
                raise forms.ValidationError('Pap smear date not known, please do not add it.')
        else:
            if (cleaned_data.get('pap_smear_date') or cleaned_data.get('pap_smear_estimate') or
               cleaned_data.get('pap_smear_result') or cleaned_data.get('pap_smear_result_status') or
               cleaned_data.get('pap_smear_result_abnormal') or cleaned_data.get('date_notified')) is not None:
                raise forms.ValidationError('Pap smear not done please do not answer questions regarding pap smear.')

    def validate_pap_smear_result(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('pap_smear_result') == YES:
            if not cleaned_data.get('pap_smear_result_status'):
                raise forms.ValidationError(
                    'Participant knows her pap smear result, please give the status of the pap smear.')
        else:
            if (cleaned_data.get('pap_smear_result_status') or cleaned_data.get('pap_smear_result_abnormal') or
               cleaned_data.get('date_notified')):
                raise forms.ValidationError(
                    'Participant pap smear result not known, no need to give pap smear status or notification date.')
    
    class Meta:
        model = MaternalContraception
        fields = '__all__'     