from dateutil.relativedelta import relativedelta
from django import forms

from ..models import MaternalUltraSoundInitial
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalUltraSoundInitialForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalUltraSoundInitialForm, self).clean()
#         cleaned_data.pop('malformations')
        self.validate_ga_by_lmp(cleaned_data)
        self.validate_ga_by_lmp(cleaned_data)
        MaternalUltraSoundInitial(
            **cleaned_data).evaluate_edd_confirmed(error_clss=forms.ValidationError)
        return cleaned_data

    def validate_est_edd_ultrasound(self, cleaned_data):
        est_edd_ultrasound = cleaned_data.get('est_edd_ultrasound')
        report_datetime = cleaned_data.get('report_datetime')
        if est_edd_ultrasound and (est_edd_ultrasound > (report_datetime.date() + relativedelta(weeks=40))):
            raise forms.ValidationError(
                'Estimated edd by ultrasound {} cannot be greater than '
                '40 weeks from today'.format(est_edd_ultrasound))

    def validate_ga_by_lmp(self, cleaned_data):
        ga_by_ultrasound_wks = cleaned_data.get('ga_by_ultrasound_wks')
        if ga_by_ultrasound_wks > 40:
            raise forms.ValidationError(
                'GA by ultrasound cannot be greater than 40 weeks.')

    class Meta:
        model = MaternalUltraSoundInitial
        fields = '__all__'
