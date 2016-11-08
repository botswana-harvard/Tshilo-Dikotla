from django import forms

from edc_constants.constants import NO, NOT_EVALUATED, YES

from td_maternal.models import MaternalConsent

from .base_infant_model_form import BaseInfantModelForm

from ..models import InfantBirthExam


class InfantBirthExamForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantBirthExamForm, self).clean()
        self.validate_report_datetime(cleaned_data, 'report_datetime')
        self.validate_general_activity(cleaned_data)
        self.validate_heent_exam(cleaned_data)
        self.validate_resp_exam(cleaned_data)
        self.validate_cardiac_exam(cleaned_data)
        self.validate_abdominal_exam(cleaned_data)
        self.validate_skin_exam(cleaned_data)
        self.validate_neuro_exam(cleaned_data)
        return cleaned_data

    def relative_identifier(self, infant_identifier):
        return RegisteredSubject.objects.get(subject_identifier=infant_identifier).relative_identifier

    def validate_report_datetime(self, cleaned_data, field):
        try:
            relative_identifier = self.relative_identifier(cleaned_data.get('infant_visit').appointment.subject_identifier)
            maternal_consent = MaternalConsent.objects.get(
                maternal_eligibility__registered_subject__subject_identifier=relative_identifier)
            if cleaned_data.get(field) < maternal_consent.consent_datetime:
                raise forms.ValidationError("{} CANNOT be before consent datetime".format(field.title()))
            if cleaned_data.get(field).date() < maternal_consent.dob:
                raise forms.ValidationError("{} CANNOT be before dob".format(field.title()))
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

    def validate_general_activity(self, cleaned_data):
        if cleaned_data.get('general_activity') == 'ABNORMAL':
            if not cleaned_data.get('abnormal_activity'):
                raise forms.ValidationError('If abnormal, please specify.')
        else:
            if cleaned_data.get('abnormal_activity'):
                raise forms.ValidationError('You indicated that there was NO abnormality in general activity, yet '
                                            'specified abnormality. Please correct')

    def validate_heent_exam(self, cleaned_data):
        if cleaned_data.get('heent_exam') == YES:
            if cleaned_data.get('heent_no_other'):
                raise forms.ValidationError(
                    'If HEENT Exam is normal, Do not answer the following Question (Q7).'
                )
        elif cleaned_data.get('heent_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('heent_no_other'):
                raise forms.ValidationError(
                    'You indicated that HEENT exam was not normal. Provide answer to Q7.'
                )

    def validate_resp_exam(self, cleaned_data):
        if cleaned_data.get('resp_exam') == YES:
            if cleaned_data.get('resp_exam_other'):
                raise forms.ValidationError(
                    'If Respiratory Exam is normal, Do not answer the following Question (Q9).'
                )
        elif cleaned_data.get('resp_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('resp_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Respiratory exam was not normal. Provide answer to Q9.'
                )

    def validate_cardiac_exam(self, cleaned_data):
        if cleaned_data.get('cardiac_exam') == YES:
            if cleaned_data.get('cardiac_exam_other'):
                raise forms.ValidationError(
                    'If Cardiac Exam is normal, Do not answer the following Question (Q11).'
                )
        elif cleaned_data.get('cardiac_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('cardiac_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Cardiac exam was not normal. Provide answer to Q11.'
                )

    def validate_abdominal_exam(self, cleaned_data):
        if cleaned_data.get('abdominal_exam') == YES:
            if cleaned_data.get('abdominal_exam_other'):
                raise forms.ValidationError(
                    'If Abdominal Exam is normal, Do not answer the following Question (Q13).'
                )
        elif cleaned_data.get('abdominal_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('abdominal_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Abdominal exam was not normal. Provide answer to Q13.'
                )

    def validate_skin_exam(self, cleaned_data):
        if cleaned_data.get('skin_exam') == YES:
            if cleaned_data.get('skin_exam_other'):
                raise forms.ValidationError(
                    'If Skin Exam is normal, Do not answer the following Question (Q15).'
                )
        elif cleaned_data.get('skin_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('skin_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Skin exam was not normal. Provide answer to Q15.'
                )

    def validate_neuro_exam(self, cleaned_data):
        if cleaned_data.get('neurologic_exam') == YES:
            if cleaned_data.get('neuro_exam_other'):
                raise forms.ValidationError(
                    'If Neurological Exam is normal, Do not answer the following Question (Q19).'
                )
        elif cleaned_data.get('neurologic_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('neuro_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Neurological exam was not normal. Provide answer to Q19.'
                )

    class Meta:
        model = InfantBirthExam
        fields = '__all__'
