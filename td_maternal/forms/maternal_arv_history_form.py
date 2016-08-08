from django import forms

from edc_constants.constants import YES, NO, STOPPED, CONTINUOUS, RESTARTED, NOT_APPLICABLE
from tshilo_dikotla.utils import weeks_between

from ..models import MaternalLifetimeArvHistory, MaternalConsent, MaternalObstericalHistory

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalLifetimeArvHistoryForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalLifetimeArvHistoryForm, self).clean()
        self.validate_if_not_on_haart()
        self.validate_haart_start_date()
        self.validate_prev_preg()
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
        if cleaned_data.get('prev_preg_haart') == YES:
            if weeks_between(haart_start_date, report_datetime.date()) < 4:
                raise forms.ValidationError(
                    "ARV start date must be four weeks prior to today's date or greater.")
        if cleaned_data.get('haart_start_date'):
            if not cleaned_data.get('is_date_estimated'):
                raise forms.ValidationError('Please answer: Is the subject\'s date of triple antiretrovirals estimated?')
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

    def validate_prev_preg(self):
        cleaned_data = self.cleaned_data
        ob_history = MaternalObstericalHistory.objects.filter(
            maternal_visit__appointment__registered_subject=cleaned_data.get(
                'maternal_visit').appointment.registered_subject)
        if not ob_history:
            raise forms.ValidationError('Please fill in the Maternal Obsterical History form first.')
        else:
            if ob_history[0].prev_pregnancies == 0:
                if cleaned_data.get('prev_preg_azt') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        'In Maternal Obsterical History form you indicated there were no previous '
                        'pregnancies. Receive AZT monotherapy in previous pregancy should be '
                        'NOT APPLICABLE')
                if cleaned_data.get('prev_sdnvp_labour') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        'In Maternal Obsterical History form you indicated there were no previous '
                        'pregnancies. Single sd-NVP in labour during a prev pregnancy should '
                        'be NOT APPLICABLE')
                if cleaned_data.get('prev_preg_haart') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        'In Maternal Obsterical History form you indicated there were no previous '
                        'pregnancies. triple ARVs during a prev pregnancy should '
                        'be NOT APPLICABLE')
                if cleaned_data.get('prev_preg_haart') == YES:
                    if not cleaned_data.get('haart_start_date'):
                        raise forms.ValidationError('Please give date triple antiretrovirals first started.')
        
    class Meta:
        model = MaternalLifetimeArvHistory
        fields = '__all__'
