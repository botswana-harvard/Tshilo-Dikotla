from edc_appointment.models import Appointment
from edc_constants.constants import YES, NO, NOT_APPLICABLE

from django import forms
from django.apps import apps as django_apps

from ..models import (MaternalArvPreg, MaternalArv, MaternalLifetimeArvHistory)
from .base_maternal_model_form import BaseMaternalModelForm


def get_previous_visit(visit_obj, timepoints, subject_identifier):
    position = timepoints.index(
        visit_obj.appointment.visit_definition.code)
    timepoints_slice = timepoints[:position]
    visit_model = django_apps.get_model(visit_obj._meta.label_lower)

    if len(timepoints_slice) > 1:
        timepoints_slice.reverse()
    for point in timepoints_slice:
        try:
            previous_appointment = Appointment.objects.filter(
                registered_subject__subject_identifier=subject_identifier, visit_definition__code=point).order_by('-created').first()
            return visit_model.objects.filter(appointment=previous_appointment).order_by('-created').first()
        except Appointment.DoesNotExist:
            pass
        except visit_model.DoesNotExist:
            pass
        except AttributeError:
            pass
    return None


class MaternalArvPregForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalArvPregForm, self).clean()
        self.validate_interrupted_medication()
        self.validate_took_yes()
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

    def validate_took_yes(self):
        cleaned_data = self.cleaned_data
        maternal_arv = self.data.get(
            'maternalarv_set-0-arv_code')
        if cleaned_data.get('took_arv') == YES:
            if not maternal_arv:
                raise forms.ValidationError(
                    {'took_arv': 'Please complete the maternal arv table.'})

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
        self.validate_previous_maternal_arv_preg_arv_start_dates()
        self.validate_stop_date_reason_for_stop()
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
            maternal_visit = cleaned_data.get(
                'maternal_arv_preg').maternal_visit
            arv_history = MaternalLifetimeArvHistory.objects.get(
                maternal_visit=maternal_visit)
            if arv_history.haart_start_date:
                start_date = cleaned_data.get('start_date')
                if start_date < arv_history.haart_start_date:
                    raise forms.ValidationError(
                        "Your ARV start date {} in this pregnancy cannot be before your "
                        "Historical ARV date {}".format(
                            start_date, arv_history.haart_start_date))
        except MaternalLifetimeArvHistory.DoesNotExist:
            pass

    def validate_previous_maternal_arv_preg_arv_start_dates(self):
        """Confirms that the ARV start date is equal to Maternal ARV
        start date unless stopped.
        """
        cleaned_data = self.cleaned_data
        subject_identifier = cleaned_data.get(
            'maternal_arv_preg').maternal_visit.appointment.registered_subject.subject_identifier
        previous_visit = get_previous_visit(
            visit_obj=cleaned_data.get('maternal_arv_preg').maternal_visit,
            timepoints=['1000M', '1020M', '2000M'],
            subject_identifier=subject_identifier)

        if previous_visit:
            previous_arv_preg = MaternalArv.objects.filter(
                maternal_arv_preg__maternal_visit__appointment__registered_subject__subject_identifier=subject_identifier,
                stop_date__isnull=True).order_by('start_date').first()
            if previous_arv_preg:
                if previous_arv_preg.start_date:
                    start_date = cleaned_data.get('start_date')
                    if start_date < previous_arv_preg.start_date:
                        raise forms.ValidationError(
                            "New start date cannot be before initial ARV start date, "
                            "initial date: {}, new start date: {}.".format(
                                previous_arv_preg.start_date, start_date))

    def validate_stop_date_reason_for_stop(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('stop_date'):
            if not cleaned_data.get('reason_for_stop'):
                raise forms.ValidationError(
                    {'reason_for_stop': 'ARV stopped, please give reason for stop.'})
        else:
            if not cleaned_data.get('stop_date'):
                if cleaned_data.get('reason_for_stop'):
                    raise forms.ValidationError(
                        {'reason_for_stop': 'ARV not stopped, do not give reason for stop.'})

    class Meta:
        model = MaternalArv
        fields = '__all__'
