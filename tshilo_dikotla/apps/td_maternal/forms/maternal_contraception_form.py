from django import forms

from edc_constants.constants import YES

from ..models import MaternalContraception
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalContraceptionForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalContraceptionForm, self).clean()
#         self.validate_more_children()
#         self.validate_next_child()
#         self.validate_uses_contraceptive()
#         self.validate_pap_smear()
#         self.validate_pap_smear_result()
        return cleaned_data

    def validate_more_children(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get('more_children') == YES:
            if (cleaned_data.get('next_child') or cleaned_data.get('contraceptive_measure') or
               cleaned_data.get('contraceptive_partner') or cleaned_data.get('contraceptive_relative')):
                raise forms.ValidationError(
                    'Participant did not answer YES to wanting more children skip to Q7.')

    def validate_next_child(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('next_child') not in ['within 2years', 'between 2-5years from now',
                                                  'More than 5years from now', 'More than 5 years from now']:
            if (cleaned_data.get('contraceptive_measure') or cleaned_data.get('contraceptive_partner') or
               cleaned_data.get('contraceptive_relative') or cleaned_data.get('influential_decision_making')):
                raise forms.ValidationError(
                    'Participant answered next child with d or e, skip to question on contraceptive method.')

    def validate_uses_contraceptive(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('uses_contraceptive') == YES:
            if not cleaned_data.get('contr'):
                raise forms.ValidationError('Participant uses a contraceptive method, please select a valid method')
        else:
            if cleaned_data.get('contr'):
                raise forms.ValidationError(
                    'Participant does not use a contraceptive method, no need to give a contraceptive method')

    def validate_pap_smear(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('pap_smear') == YES:
            if not cleaned_data.get('pap_smear_date'):
                raise forms.ValidationError('Please give the date the pap smear was done.')
        else:
            if (cleaned_data.get('pap_smear_date'), cleaned_data.get('pap_smear_estimate') or
               cleaned_data.get('pap_smear_result') or cleaned_data.get('pap_smear_result_status') or
               cleaned_data.get('pap_smear_result_abnormal') or cleaned_data.get('date_notified')):
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
