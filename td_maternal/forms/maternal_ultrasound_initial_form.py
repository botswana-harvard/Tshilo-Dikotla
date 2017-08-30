from django import forms

from ..models import MaternalUltraSoundInitial
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalUltraSoundInitialForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalUltraSoundInitialForm, self).clean()
#         cleaned_data.pop('malformations')
        self.validate_ga_by_lmp(cleaned_data)
        MaternalUltraSoundInitial(
            **cleaned_data).evaluate_edd_confirmed(error_clss=forms.ValidationError)
        return cleaned_data

    def validate_ga_by_lmp(self, cleaned_data):
        ga_by_lmp = cleaned_data.get('ga_by_lmp')
        report_datetime = cleaned_data.get('report_datetime')
        if ga_by_lmp and (ga_by_lmp > (report_datetime.date() + report_datetime(weeks=40))):
            raise forms.ValidationError(
                'Got GA by LMP as {} and report datetime as {}'.format(ga_by_lmp, report_datetime))

    class Meta:
        model = MaternalUltraSoundInitial
        fields = '__all__'
