from dateutil.relativedelta import relativedelta
from django import forms

from td_maternal.models.enrollment_helper import EnrollmentHelper

from ..models import AntenatalEnrollment, MaternalEligibility
from ..models import TdConsentVersion, MaternalConsent

from .base_enrollment_form import BaseEnrollmentForm


class AntenatalEnrollmentForm(BaseEnrollmentForm):

    def clean(self):
        cleaned_data = super(AntenatalEnrollmentForm, self).clean()
        self.validate_last_period_date(
            cleaned_data.get('report_datetime'), cleaned_data.get('last_period_date'))
        enrollment_helper = EnrollmentHelper(instance_antenatal=self._meta.model(**cleaned_data),
                                             exception_cls=forms.ValidationError)
        enrollment_helper.raise_validation_error_for_rapidtest()

        return cleaned_data

    def validate_last_period_date(self, report_datetime, last_period_date):
        if last_period_date and (last_period_date > (report_datetime.date() - relativedelta(weeks=16))):
            raise forms.ValidationError('LMP cannot be within 16weeks of report datetime. '
                                        'Got LMP as {} and report datetime as {}'.format(last_period_date,
                                                                                         report_datetime))
        elif last_period_date and (last_period_date <= report_datetime.date() - relativedelta(weeks=37)):
            raise forms.ValidationError('LMP cannot be more than 36weeks of report datetime. '
                                        'Got LMP as {} and report datetime as {}'.format(last_period_date,
                                                                                         report_datetime))

    def clean_rapid_test_date(self):
        rapid_test_date = self.cleaned_data['rapid_test_date']
        registered_subject = self.cleaned_data['registered_subject']
        if rapid_test_date:
            try:
                initial = AntenatalEnrollment.objects.get(
                    registered_subject=registered_subject)
                if initial:
                    if rapid_test_date != initial.rapid_test_date:
                        raise forms.ValidationError(
                            'The rapid test result cannot be changed')
            except AntenatalEnrollment.DoesNotExist:
                pass
        return rapid_test_date

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
                    'Complete Maternal Consent form for version {} before '
                    'proceeding'.format(td_consent_version.version))

    @property
    def maternal_eligibility(self):
        cleaned_data = self.cleaned_data
        subject_identifier = cleaned_data.get(
            'registered_subject').subject_identifier
        try:
            return MaternalEligibility.objects.get(
                registered_subject__subject_identifier=subject_identifier)
        except MaternalEligibility.DoesNotExist:
            return None

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
