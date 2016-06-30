from django import forms
from edc_constants.constants import YES, POS, NEG, IND

from .base_maternal_model_form import BaseMaternalModelForm
from ..models import RapidTestResult


class RapidTestResultForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(BaseMaternalModelForm, self).clean()
        self.validate_date_for_rapid_test()
        self.validate_result_of_rapid_test()
        self.validate_result_date_must_not_be_provided()
        self.validate_rapid_test_result_present_no_rapid_test_done()
        return cleaned_data
    
    def validate_date_for_rapid_test(self):
        cleaned_data=self.cleaned_data
        if cleaned_data.get('rapid_test_done') == YES:
            if not cleaned_data.get('result_date'):
                raise forms.ValidationError(
                    'If a rapid test was processed, what is the date'
                    ' of the rapid test?')
        
    def validate_result_of_rapid_test(self):
        cleaned_data=self.cleaned_data
        if not cleaned_data.get('result') in [POS, NEG, IND]:
            raise forms.ValidationError(
                    'If a rapid test was processed, what is the test result?')
     
    def validate_result_date_must_not_be_provided(self):
        cleaned_data=self.cleaned_data
        if cleaned_data.get('result_date'):
            raise forms.ValidationError(
                    'If a rapid test was not processed, please do not provide the result date. ')
    
    def validate_rapid_test_result_present_no_rapid_test_done(self):
        cleaned_data=self.cleaned_data
        if cleaned_data.get('result'):
            raise forms.ValidationError(
                    'If a rapid test was not processed, please do not provide the result. ')

    class Meta:
        model = RapidTestResult
        fields = '__all__'
