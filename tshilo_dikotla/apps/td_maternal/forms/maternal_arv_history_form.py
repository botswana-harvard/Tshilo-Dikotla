from django import forms

from edc_constants.constants import NO, STOPPED, CONTINUOUS, RESTARTED
from tshilo_dikotla.apps.td.utils import weeks_between

from ..models import MaternalLifetimeArvHistory, MaternalConsent

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalLifetimeArvHistoryForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalLifetimeArvHistoryForm, self).clean()
        self.validate_if_not_on_haart()
        self.validate_haart_start_date()
        return cleaned_data

    def validate_if_not_on_haart(self):
        """Confirms that HAART is not continuous or stopped if reported as not on haart."""
        cleaned_data = self.cleaned_data
        if cleaned_data.get('preg_on_haart') == NO:
            if cleaned_data.get('prior_preg') == RESTARTED:
                raise forms.ValidationError(
                    'You indicated that the mother was NOT on triple ARV when she '
                    'got pregnant. ARVs could not have been interrupted. Please correct.')
            if cleaned_data.get('prior_preg') == CONTINUOUS:
                raise forms.ValidationError(
                    'You indicated that the mother was NOT on triple ARV when she '
                    'got pregnant. ARVs could not have been uninterrupted. Please correct.')
        else:
            if cleaned_data.get('prior_preg') == STOPPED:
                raise forms.ValidationError(
                    'You indicated that the mother was still on triple ARV when '
                    'she got pregnant, yet you indicated that ARVs were interrupted '
                    'and never restarted. Please correct.')

    def validate_haart_start_date(self):
        cleaned_data = self.cleaned_data
        report_datetime = cleaned_data.get("report_datetime")
        haart_start_date = cleaned_data.get('haart_start_date')
        if weeks_between(haart_start_date, report_datetime.date()) < 6:
            raise forms.ValidationError(
                "ARV start date must be six weeks prior to today's date or greater.")
        try:
            maternal_consent = MaternalConsent.objects.get(
                registered_subject__subject_identifier=cleaned_data.get(
                    'maternal_visit').appointment.registered_subject.subject_identifier)
            if report_datetime < maternal_consent.consent_datetime:
                raise forms.ValidationError("Report datetime CANNOT be before consent datetime")
            if haart_start_date < maternal_consent.dob:
                raise forms.ValidationError("Date of triple ARVs first started CANNOT be before DOB.")
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

    class Meta:
        model = MaternalLifetimeArvHistory
        fields = '__all__'
