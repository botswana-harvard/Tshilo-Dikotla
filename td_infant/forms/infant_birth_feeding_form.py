from django import forms

from ..models import InfantBirthFeedingVaccine, InfantVaccines

from .base_infant_model_form import BaseInfantModelForm

from td_maternal.models import MaternalConsent
from ..models import InfantBirth


class InfantBirthFeedinVaccineForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantBirthFeedinVaccineForm, self).clean()
#         self.validate_report_datetime(cleaned_data)
        return cleaned_data

    def validate_report_datetime(self, cleaned_data):
        try:
            dob = cleaned_data.get('infant_visit').appointment.registered_subject.dob
            if cleaned_data.get('report_datetime').date() < dob:
                raise forms.ValidationError(
                    'Report date {} cannot be before infant DOB of {}'.format(
                        cleaned_data.get('report_datetime').date(),
                        cleaned_data.get('infant_visit').appointment.registered_subject.dob))
            relative_identifier = cleaned_data.get(
                'infant_visit').appointment.registered_subject.relative_identifier
            maternal_consent = MaternalConsent.objects.filter(
                registered_subject__subject_identifier=relative_identifier).order_by('consent_datetime').last()
            if cleaned_data.get('report_datetime') < maternal_consent.consent_datetime:
                raise forms.ValidationError(
                    "Report date of {} CANNOT be before consent datetime".format(
                        cleaned_data.get('report_datetime')))
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

    class Meta:
        model = InfantBirthFeedingVaccine
        fields = '__all__'


class InfantVaccinesForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantVaccinesForm, self).clean()
#         dob = cleaned_data.get('infant_birth_feed_vaccine').infant_visit.appointment.registered_subject.dob
#         if cleaned_data.get('vaccine_date') < dob:
#                 raise forms.ValidationError(
#                     'Vaccine date {} cannot be before infant DOB of {}'.format(
#                         cleaned_data.get('vaccine_date'),
#                         cleaned_data.get(
#                             'infant_birth_feed_vaccine').infant_visit.appointment.registered_subject.dob))
#         self.validate_vaccine_date()
        return cleaned_data

    def validate_vaccine_date(self):
        cleaned_data = self.cleaned_data
        try:
            subject_identifier = cleaned_data.get(
                'infant_birth_feed_vaccine').infant_visit.appointment.registered_subject.subject_identifier
            infant_birth = InfantBirth.objects.get(registered_subject__subject_identifier=subject_identifier)
            if cleaned_data.get('vaccine_date') < infant_birth.dob:
                raise forms.ValidationError('Vaccine date CANNOT be before DOB.')
        except InfantBirth.DoesNotExist:
            raise forms.ValidationError('Infant Birth does not exist.')

    class Meta:
        model = InfantVaccines
        fields = '__all__'
