from dateutil import rrule

from django import forms
from django.core.exceptions import FieldError

from edc_constants.constants import POS, NEG, NOT_APPLICABLE, YES, NO, DWTA, UNKNOWN, NEVER

from .models import MaternalConsent, SpecimenConsent


class EnrollmentFormMixin(forms.ModelForms):

    """TODO: this does nothing."""

    def clean(self):
        cleaned_data = super(EnrollmentFormMixin, self).clean()
#         self.requires_specimen_consent()
#         self.requires_rapid_test_if_current_hiv_status_uknown()
#         self.requires_week32_result_if_tested()
#         self.neg_current_hiv_status_and_test_and_regimen()
#         self.pos_current_hiv_status_and_test_and_regimen()
#         self.valid_regimen_and_duration()
#         self.week32_test_matches_current()
#         self.rapid_test_date_and_result()
#         self.raise_if_rapid_test_required()
#         self.raise_if_rapid_test_date_future()
#         EnrollmentHelper(instance_antenatal=self._meta.model(**cleaned_data), exception_cls=forms.ValidationError)
        return cleaned_data

    def clean_report_datetime(self):
        report_datetime = self.cleaned_data['report_datetime']
        maternal_consent = self.get_consent_or_raise(MaternalConsent)
        if report_datetime < maternal_consent.consent_datetime:
            raise forms.ValidationError(
                'Report datetime \'{}\' cannot be before the consent datetime of {}. '
                'Please correct'.format(
                    report_datetime,
                    maternal_consent.consent_datetime))
        return report_datetime

    def clean_registered_subject(self):
        registered_subject = self.cleaned_data['registered_subject']
        if not registered_subject:
            raise forms.ValidationError('Expected a registered subject. Got None.')
        return registered_subject

    def requires_specimen_consent(self):
        self.get_consent_or_raise(SpecimenConsent)

    def raise_if_rapid_test_required(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('current_hiv_status') == NEG and cleaned_data.get('week32_test_date'):
            weeks_since_test = self.weeks_since_test(
                cleaned_data.get('week32_test_date'), cleaned_data.get('report_datetime'))
            if weeks_since_test < 32 and cleaned_data.get('rapid_test_done') == NO:
                    raise forms.ValidationError(
                        "Rapid test is required. Participant tested > 32 weeks ago.")

    def weeks_since_test(self, week32_test_date, report_datetime):
        """Returns the number of weeks since the last HIV test.

        Only relevant for tests with a NEG result."""
        cleaned_data = self.cleaned_data
        weeks = rrule.rrule(
            rrule.WEEKLY, dtstart=week32_test_date, until=report_datetime.date()).count()
        weeks_since_test = cleaned_data.get(self.Meta.model.weeks_base_field) - weeks
        return weeks_since_test

    def requires_rapid_test_if_current_hiv_status_uknown(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('current_hiv_status') in [NEVER, UNKNOWN, DWTA]:
            if cleaned_data.get('rapid_test_done') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'The current HIV status is {}. Rapid test cannot be NOT APPLICABLE.'.format(
                        cleaned_data.get('current_hiv_status')))
            if cleaned_data.get('rapid_test_done') == NO:
                raise forms.ValidationError(
                    "Participant current HIV status is {}. You must "
                    "conduct HIV rapid testing today to continue with "
                    "the eligibility screen".format(cleaned_data.get('current_hiv_status')))

    def requires_week32_result_if_tested(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get("week32_test") == YES:
            if not cleaned_data.get("week32_result"):
                raise forms.ValidationError('Please provide test result at week 32.')
        else:
            if cleaned_data.get("week32_result"):
                raise forms.ValidationError(
                    'You mentioned testing was not done at 32weeks yet provided a test result.')

    def week32_test_matches_current(self):
        cleaned_data = self.cleaned_data
        if ((cleaned_data.get("week32_result") == POS and cleaned_data.get("current_hiv_status") != POS) or
                (cleaned_data.get("week32_result") == NEG and cleaned_data.get("current_hiv_status") != NEG)):
            raise forms.ValidationError('The current hiv status and result at 32weeks should be the same!')

    def neg_current_hiv_status_and_test_and_regimen(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('current_hiv_status') == NEG:
            if cleaned_data.get('evidence_hiv_status') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated that the participant is Negative, Evidence of HIV '
                    'result CANNOT be \'Not Applicable\'. Please correct.')
            if not cleaned_data.get('valid_regimen') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated that the participant is Negative.'
                    ' Answer for REGIMEN should be \'Not Applicable\'.')
            if not cleaned_data.get('valid_regimen_duration') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated that the participant is Negative.'
                    ' Answer for REGIMEN DURATION should be \'Not Applicable\'.')
            if cleaned_data.get('evidence_hiv_status') == NO:
                if not cleaned_data.get('rapid_test_done') == YES:
                    raise forms.ValidationError("Participant is NEG and has no doc evidence. "
                                                "Rapid test is REQUIRED. Please Correct")

    def pos_current_hiv_status_and_test_and_regimen(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('current_hiv_status') == POS:
            if cleaned_data.get('evidence_hiv_status') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated that the participant is Positive, Evidence of HIV '
                    'result CANNOT be \'Not Applicable\'. Please correct.')
            if cleaned_data.get('valid_regimen') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated that the participant is Positive, \'do records show that'
                    ' participant takes ARVs\' cannot be \'Not Applicable\'.')
            if cleaned_data.get('evidence_hiv_status') == YES:
                if cleaned_data.get('rapid_test_done') == YES:
                    raise forms.ValidationError(
                        'There is no need for a rapid test. Subject is positive and has evidence.')

    def valid_regimen_and_duration(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('valid_regimen') == YES:
            if cleaned_data.get('valid_regimen_duration') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated that the participant is on ARV. Regimen validity period'
                    ' CANNOT be \'Not Applicable\'. Please correct.')
        else:
            if cleaned_data.get('valid_regimen_duration') != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated that there are no records of Participant taking ARVs. '
                    'Regimen validity period should be \'Not Applicable\'. Please correct.')

    def get_consent_or_raise(self, model_class):
        cleaned_data = self.cleaned_data
        obj = None
        try:
            obj = model_class.objects.get(
                subject_identifier=cleaned_data.get(
                    'registered_subject').subject_identifier)
        except (FieldError, AttributeError):
            print ("get_consent_or_raise", cleaned_data.get('registered_subject'))
            obj = model_class.objects.get(
                maternal_eligibility__registered_subject__subject_identifier=cleaned_data.get(
                    'registered_subject').subject_identifier)
        except model_class.DoesNotExist:
            raise forms.ValidationError(
                "Please ensure to save the {} before "
                "completing Enrollment".format(model_class._meta.verbose_name))
        return obj

    def rapid_test_date_and_result(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('rapid_test_done') == YES:
            # date of rapid test is required if rapid test processed is indicated as Yes
            if not cleaned_data.get('rapid_test_date'):
                raise forms.ValidationError(
                    'You indicated that a rapid test was processed. Please provide the date.')
            # if rapid test was done, result should be indicated
            if not cleaned_data.get('rapid_test_result'):
                raise forms.ValidationError(
                    'You indicated that a rapid test was processed. Please provide a result.')
        else:
            if cleaned_data.get('rapid_test_date'):
                raise forms.ValidationError(
                    'You indicated that a rapid test was NOT processed, yet rapid test date was'
                    ' provided. Please correct.')
            if cleaned_data.get('rapid_test_result'):
                raise forms.ValidationError(
                    'You indicated that a rapid test was NOT processed, yet rapid test result '
                    'was provided. Please correct.')

    def raise_if_rapid_test_date_future(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('rapid_test_date'):
            if cleaned_data.get('rapid_test_date') > cleaned_data.get('report_datetime').date():
                raise forms.ValidationError(
                    'Rapid test date cannot be a future date relative to the report date')
