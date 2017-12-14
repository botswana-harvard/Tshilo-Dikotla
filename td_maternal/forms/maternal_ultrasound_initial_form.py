from dateutil.relativedelta import relativedelta
from django import forms

from ..models import MaternalUltraSoundInitial
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalUltraSoundInitialForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalUltraSoundInitialForm, self).clean()
#         cleaned_data.pop('malformations')
        self.validate_est_edd_ultrasound(cleaned_data)
        self.validate_ga_by_lmp(cleaned_data)
        self.validate_ga_by_ultrasound_against_est_edd_ultrasound(cleaned_data)
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

    def validate_ga_by_ultrasound_against_est_edd_ultrasound(self, cleaned_data):
        est_edd = cleaned_data.get('est_edd_ultrasound')
        ga_by_ultrasound = cleaned_data.get('ga_by_ultrasound_wks')
        est_edd_ultrasound = cleaned_data.get('est_edd_ultrasound')
        report_datetime = cleaned_data.get('report_datetime')
        if cleaned_data.get('ga_by_ultrasound_wks'):
            est_conceive_date = (report_datetime.date(
            ) - relativedelta(weeks=ga_by_ultrasound))
            weeks_between = ((est_edd - est_conceive_date).days) / 7
            if (weeks_between + 1) > ga_by_ultrasound:
                if (int(weeks_between) + 1) not in range(38, 42):
                    raise forms.ValidationError(
                        'Estimated edd by ultrasound {} should match '
                        'GA by ultrasound'.format(est_edd_ultrasound))

    class Meta:
        model = MaternalUltraSoundInitial
        fields = '__all__'
