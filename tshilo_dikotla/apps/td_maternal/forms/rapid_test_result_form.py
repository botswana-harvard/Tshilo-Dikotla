from django import forms
from edc_constants.constants import YES, POS, NEG, IND

from .base_maternal_model_form import BaseMaternalModelForm
from ..models import RapidTestResult


class RapidTestResultForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(BaseMaternalModelForm, self).clean()
        if cleaned_data.get('rapid_test_done') == YES:
            if not cleaned_data.get('result_date'):
                raise forms.ValidationError(
                    'If a rapid test was processed, what is the date'
                    ' of the rapid test?')
            elif not cleaned_data.get('result') in [POS, NEG, IND]:
                raise forms.ValidationError(
                    'If a rapid test was processed, what is the test result?')
        else:
            if cleaned_data.get('result_date') or cleaned_data.get('result'):
                raise forms.ValidationError(
                    'If a rapid test was not processed, please do not provide the result date. '
                    'Got {}.'.format(cleaned_data.get('result_date')))
            elif cleaned_data.get('result'):
                raise forms.ValidationError(
                    'If a rapid test was not processed, please do not provide the result. '
                    'Got {}.'.format(cleaned_data.get('result')))
        return cleaned_data

    class Meta:
        model = RapidTestResult
        fields = '__all__'
