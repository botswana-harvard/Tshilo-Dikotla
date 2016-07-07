from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_base.form.old_forms import BaseModelForm
from edc_constants.constants import ON_STUDY
from edc_visit_tracking.forms import VisitFormMixin

from tshilo_dikotla.apps.td.choices import VISIT_REASON, VISIT_INFO_SOURCE, INFANT_VISIT_STUDY_STATUS, INFO_PROVIDER
from tshilo_dikotla.apps.td_maternal.models import MaternalConsent, MaternalDeathReport

from ..models import InfantVisit


class InfantVisitForm(VisitFormMixin, BaseModelForm):

    participant_label = 'infant'

    information_provider = forms.ChoiceField(
        label='Please indicate who provided most of the information for this infant\'s visit',
        choices=INFO_PROVIDER,
        initial='MOTHER',
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    study_status = forms.ChoiceField(
        label='What is the infant\'s current study status',
        choices=INFANT_VISIT_STUDY_STATUS,
        initial=ON_STUDY,
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    info_source = forms.ChoiceField(
        required=False,
        label='Source of information',
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        cleaned_data = super(InfantVisitForm, self).clean()
#         self.validate_reason_visit_missed()
#         self.validate_report_datetime_and_consent()
#         self.validate_information_provider_is_alive()
        return cleaned_data

    def validate_report_datetime_and_consent(self):
        cleaned_data = self.cleaned_data
        try:
            relative_identifier = cleaned_data.get('appointment').registered_subject.relative_identifier
            maternal_consent = MaternalConsent.objects.get(
                registered_subject__subject_identifier=relative_identifier)
            if cleaned_data.get("report_datetime") < maternal_consent.consent_datetime:
                raise forms.ValidationError("Report datetime cannot be before consent datetime")
            if cleaned_data.get("report_datetime").date() < maternal_consent.dob:
                raise forms.ValidationError("Report datetime cannot be before DOB")
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal consent does not exist.')

    def validate_information_provider_is_alive(self):
        cleaned_data = self.cleaned_data
        try:
            if cleaned_data.get('information_provider') == 'MOTHER':
                relative_identifier = cleaned_data.get('appointment').registered_subject.relative_identifier
                maternal_death_report = MaternalDeathReport.objects.get(
                    maternal_visit__appointment__registered_subject__subject_identifier=relative_identifier,
                    death_date__lte=cleaned_data.get("report_datetime").date())
                raise forms.ValidationError(
                    'The mother was reported deceased on {}.'
                    'The information provider cannot be the \'mother\'.'.format(
                        maternal_death_report.death_date.strftime('%Y-%m-%d')))
        except MaternalDeathReport.DoesNotExist:
            pass

    class Meta:
        model = InfantVisit
        fields = '__all__'
