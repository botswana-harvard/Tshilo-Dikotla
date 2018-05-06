from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_base.form.old_forms import BaseModelForm
from edc_constants.constants import ON_STUDY
from edc_visit_tracking.forms import VisitFormMixin

from tshilo_dikotla.choices import VISIT_REASON, VISIT_INFO_SOURCE, INFANT_VISIT_STUDY_STATUS, INFO_PROVIDER
from td_maternal.models import MaternalConsent, MaternalDeathReport, TdConsentVersion

from ..models import InfantVisit
from td_maternal.models.maternal_eligibility import MaternalEligibility


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
        self.validate_current_consent_version()
#         self.validate_reason_visit_missed()
#         self.validate_report_datetime_and_consent()
#         self.validate_information_provider_is_alive()
        return cleaned_data

    def validate_report_datetime_and_consent(self):
        cleaned_data = self.cleaned_data
        try:
            relative_identifier = cleaned_data.get(
                'appointment').registered_subject.relative_identifier
            maternal_consent = MaternalConsent.objects.filter(
                registered_subject__subject_identifier=relative_identifier).order_by('consent_datetime').last()
            if cleaned_data.get("report_datetime") < maternal_consent.consent_datetime:
                raise forms.ValidationError(
                    "Report datetime cannot be before consent datetime")
            if cleaned_data.get("report_datetime").date() < maternal_consent.dob:
                raise forms.ValidationError(
                    "Report datetime cannot be before DOB")
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal consent does not exist.')

    def validate_information_provider_is_alive(self):
        cleaned_data = self.cleaned_data
        try:
            if cleaned_data.get('information_provider') == 'MOTHER':
                relative_identifier = cleaned_data.get(
                    'appointment').registered_subject.relative_identifier
                maternal_death_report = MaternalDeathReport.objects.get(
                    maternal_visit__appointment__registered_subject__subject_identifier=relative_identifier,
                    death_date__lte=cleaned_data.get("report_datetime").date())
                raise forms.ValidationError(
                    'The mother was reported deceased on {}.'
                    'The information provider cannot be the \'mother\'.'.format(
                        maternal_death_report.death_date.strftime('%Y-%m-%d')))
        except MaternalDeathReport.DoesNotExist:
            pass

    def validate_current_consent_version(self):
        try:
            td_consent_version = TdConsentVersion.objects.get(
                maternal_eligibility=self.maternal_eligibility)
        except TdConsentVersion.DoesNotExist:
            raise forms.ValidationError(
                'Complete mother\'s consent version form before proceeding')
        else:
            try:
                MaternalConsent.objects.get(
                    maternal_eligibility=self.maternal_eligibility,
                    version=td_consent_version.version)
            except MaternalConsent.DoesNotExist:
                raise forms.ValidationError(
                    f'Maternal Consent form for version {td_consent_version.version} before proceeding')

    @property
    def maternal_eligibility(self):
        cleaned_data = self.cleaned_data
        relative_identifier = cleaned_data.get(
            'appointment').registered_subject.relative_identifier
        try:
            return MaternalEligibility.objects.get(
                registered_subject__subject_identifier=relative_identifier)
        except MaternalEligibility.DoesNotExist:
            pass

    class Meta:
        model = InfantVisit
        fields = '__all__'
