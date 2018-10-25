from django import forms
from django.forms.utils import ErrorList

from edc_constants.constants import NO, YES

from ..models import MaternalSrh

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalSrhForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalSrhForm, self).clean()
        if cleaned_data.get('is_contraceptive_initiated') == YES:
            self.validate_m2m(
                label='contraceptive method',
                leading=cleaned_data.get('is_contraceptive_initiated'),
                m2m=cleaned_data.get('contr'))
        self.validate_unseen_at_clinic()
        self.validate_not_tried()
        self.validate_contraceptive_initiated()
        return cleaned_data

    def validate_unseen_at_clinic(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('seen_at_clinic') == NO:
            if not cleaned_data.get('reason_unseen_clinic'):
                raise forms.ValidationError(
                    {'reason_unseen_clinic':
                     'If you have not been seen in that clinic since your last visit with us, why not?'})
        if cleaned_data.get('seen_at_clinic') == 'DWTA':
            if (cleaned_data.get('reason_unseen_clinic') or
                cleaned_data.get('is_contraceptive_initiated') or
                cleaned_data.get('contr') or
                cleaned_data.get('reason_not_initiated') or
                    cleaned_data.get('srh_referral')):
                raise forms.ValidationError(
                    {'reason_not_initiated':
                     'If participant does not want to answer, the questionnaire is complete.'})

    def validate_not_tried(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('reason_unseen_clinic') == 'not_tried':
            if (cleaned_data.get('is_contraceptive_initiated') or
                cleaned_data.get('contr') or
                cleaned_data.get('reason_not_initiated') or
                    cleaned_data.get('srh_referral')):
                raise forms.ValidationError(
                    {'reason_unseen_clinic':
                     'If Q3 is \'No\' all Questions after Question 4 must None or Blank.'})

    def validate_contraceptive_initiated(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('is_contraceptive_initiated') == YES:
            if not cleaned_data.get('contr'):
                raise forms.ValidationError(
                    {'contr':
                     'You indicated that contraceptives were initiated, please give a valid contraceptive.'})
            if cleaned_data.get('reason_not_initiated'):
                raise forms.ValidationError(
                    {'reason_not_initiated'
                     'You indicated that contraceptives were initiated, please do not give reason not initiated.'})
        if cleaned_data.get('is_contraceptive_initiated') == NO:
            if not cleaned_data.get('reason_not_initiated'):
                self._errors["reason_not_initiated"] = ErrorList(
                    ["This field is required."])
                raise forms.ValidationError(
                    {'reason_not_initiated':
                     'If you have not initiated contraceptive method, please provide reason.'})
        if cleaned_data.get('is_contraceptive_initiated') == 'DWTA':
            if cleaned_data.get('contr') or cleaned_data.get('reason_not_initiated'):
                raise forms.ValidationError(
                    {'reason_not_initiated':
                     'Participant does not want to answer the question on contraceptive initiation, '
                     'the questionnaire is complete.'})

    class Meta:
        model = MaternalSrh
        fields = '__all__'
