from dateutil.parser import parse as parse_date
from django import forms
from django.utils import timezone

from edc_constants.constants import YES, NO, NOT_APPLICABLE
from tshilo_dikotla.utils import weeks_between

from ..models import (MaternalArvPreg, MaternalArv, MaternalLifetimeArvHistory, PostnatalEnrollment,
                      AntenatalEnrollment)

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalArvPregForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalArvPregForm, self).clean()
        self.validate_interrupted_medication()
        return cleaned_data

    def validate_interrupted_medication(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('is_interrupt') == YES and
                cleaned_data.get('interrupt') == NOT_APPLICABLE):
            raise forms.ValidationError('You indicated that ARVs were interrupted during pregnancy. '
                                        'Please provide a reason for interruption')
        if (cleaned_data.get('is_interrupt') == NO and
                cleaned_data.get('interrupt') != NOT_APPLICABLE):
            raise forms.ValidationError('You indicated that ARVs were NOT interrupted during '
                                        'pregnancy. You cannot provide a reason. Please correct.')

#     def validate_arv_exposed(self):
#         cleaned_data = self.cleaned_data
#         if cleaned_data.get('took_arv') == NO:
#             registered_subject = cleaned_data.get('maternal_visit').appointment.registered_subject
#             try:
#                 antental = AntenatalEnrollment.objects.get(registered_subject=registered_subject)
#                 if antental.valid_regimen_duration == YES:
#                     raise forms.ValidationError(
#                         "At ANT you indicated that the participant has been on regimen "
#                         "for period of time. But now you indicated that the participant did not "
#                         "take ARVs. Please Correct.")
#             except AntenatalEnrollment.DoesNotExist:
#                 pass
#             try:
#                 postnatal = PostnatalEnrollment.objects.get(registered_subject=registered_subject)
#                 if postnatal.valid_regimen_duration == YES:
#                     raise forms.ValidationError(
#                         "At PNT you indicated that the participant has been on regimen "
#                         "for period of time. But now you indicated that the participant did not "
#                         "take ARVs. Please Correct.")
#             except PostnatalEnrollment.DoesNotExist:
#                 pass

    class Meta:
        model = MaternalArvPreg
        fields = '__all__'


class MaternalArvForm(BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(MaternalArvForm, self).clean()
        self.validate_start_stop_date()
        self.validate_took_arv()
        self.validate_historical_and_present_arv_start_dates()
        return cleaned_data

    def validate_start_stop_date(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('stop_date'):
            if cleaned_data.get('stop_date') < cleaned_data.get('start_date'):
                raise forms.ValidationError(
                    'Your stop date of {} is prior to start date of {}. '
                    'Please correct'.format(
                        cleaned_data.get('stop_date'), cleaned_data.get('start_date')))

    def validate_took_arv(self):
        cleaned_data = self.cleaned_data
        took_arv = cleaned_data.get('maternal_arv_preg').took_arv
        if took_arv == YES:
            if not cleaned_data.get('arv_code'):
                raise forms.ValidationError(
                    "You indicated that participant started ARV(s) during this "
                    "pregnancy. Please list them on 'Maternal ARV' table")
        else:
            if cleaned_data.get('arv_code'):
                raise forms.ValidationError(
                    "You indicated that ARV(s) were NOT started during this pregnancy. "
                    "You cannot provide a list. Please Correct.")

    def validate_historical_and_present_arv_start_dates(self):
        """Confirms that the ARV start date is not less than the Historical ARV start date"""
        cleaned_data = self.cleaned_data
        try:
            maternal_visit = cleaned_data.get('maternal_arv_preg').maternal_visit
            arv_history = MaternalLifetimeArvHistory.objects.get(maternal_visit=maternal_visit)
            if arv_history.haart_start_date:
                start_date = cleaned_data.get('start_date')
                if start_date < arv_history.haart_start_date:
                    raise forms.ValidationError(
                        "Your ARV start date {} in this pregnancy cannot be before your "
                        "Historical ARV date {}".format(
                            start_date, arv_history.haart_start_date))
        except MaternalLifetimeArvHistory.DoesNotExist:
            pass

    class Meta:
        model = MaternalArv
        fields = '__all__'
