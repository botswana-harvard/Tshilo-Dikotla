from django import forms

from edc_constants.constants import NO, NOT_EVALUATED, YES

from td_maternal.models import MaternalConsent

from ..models import InfantFuPhysical, InfantBirth

from .base_infant_model_form import BaseInfantModelForm


class InfantFuPhysicalForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantFuPhysicalForm, self).clean()
        self.validate_height()
        self.validate_head_circum()
        self.validate_report_datetime()
        self.validate_general_activity()
        self.validate_heent_exam()
        self.validate_resp_exam()
        self.validate_cardiac_exam()
        self.validate_abdominal_exam()
        self.validate_skin_exam()
        self.validate_neuro_exam()
        return cleaned_data

    def validate_height(self):
        cleaned_data = self.cleaned_data
        visit = ['2000', '2010', '2020', '2060', '2120', '2180', '2240', '2300', '2360']

        if (not cleaned_data.get('infant_visit').appointment.visit_code == '2000' and
                not cleaned_data.get('infant_visit').appointment.visit_code == '2010'):
            prev_visit = visit.index(cleaned_data.get('infant_visit').appointment.visit_code) - 1
            while prev_visit > 0:
                try:
                    subject_identifier = cleaned_data.get('infant_visit').appointment.subject_identifier
                    prev_fu_phy = InfantFuPhysical.objects.get(
                        infant_visit__appointment__subject_identifier=subject_identifier,
                        infant_visit__appointment__visit_code=visit[prev_visit])
                    if cleaned_data.get('height') < prev_fu_phy.height:
                        raise forms.ValidationError(
                            'You stated that the height for the participant as {}, yet in visit {} '
                            'you indicated that participant height was {}. Please correct.'.format(
                                cleaned_data.get('height'), visit[prev_visit], prev_fu_phy.height))
                    break
                except InfantFuPhysical.DoesNotExist:
                    prev_visit = prev_visit - 1

    def validate_head_circum(self):
        cleaned_data = self.cleaned_data
        visit = ['2000', '2010', '2020', '2060', '2120', '2180', '2240', '2300', '2360']

        if (not cleaned_data.get('infant_visit').appointment.visit_code == '2000' and
                not cleaned_data.get('infant_visit').appointment.visit_code == '2000'):
            prev_visit = visit.index(cleaned_data.get('infant_visit').appointment.visit_code) - 1
            while prev_visit > 0:
                try:
                    subject_identifier = cleaned_data.get('infant_visit').appointment.subject_identifier
                    prev_fu_phy = InfantFuPhysical.objects.get(
                        infant_visit__appointment__subject_identifier=subject_identifier,
                        infant_visit__appointment__visit_code=visit[prev_visit])
                    if cleaned_data.get('head_circumference') < prev_fu_phy.head_circumference:
                        raise forms.ValidationError(
                            'You stated that the head circumference for the participant as {}, '
                            'yet in visit {} you indicated that participant height was {}. '
                            'Please correct.'.format(
                                cleaned_data.get('head_circumference'),
                                visit[prev_visit], prev_fu_phy.head_circumference))
                    break
                except InfantFuPhysical.DoesNotExist:
                    prev_visit = prev_visit - 1

    def validate_report_datetime(self):
        cleaned_data = self.cleaned_data
        try:
            subject_identifier = cleaned_data.get('infant_visit').appointment.subject_identifier
            infant_birth = InfantBirth.objects.get(registered_subject__subject_identifier=subject_identifier)
            if (cleaned_data.get('report_datetime').date() <
                    infant_birth.dob):
                raise forms.ValidationError('Report date {} cannot be before infant DOB of {}'.format(
                    cleaned_data.get('report_datetime').date(),
                    infant_birth.registered_subject.dob))
            maternal_consent = MaternalConsent.objects.get(
                maternal_eligibility__registered_subject__subject_identifier=infant_birth.registered_subject.relative_identifier)
            if cleaned_data.get('report_datetime') < maternal_consent.consent_datetime:
                raise forms.ValidationError(
                    "Report date of {} CANNOT be before consent datetime".format(cleaned_data.get('report_datetime')))
        except InfantBirth.DoesNotExist:
            raise forms.ValidationError('Infant Birth does not exist.')
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

    def validate_general_activity(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('general_activity') == 'ABNORMAL':
            if not cleaned_data.get('abnormal_activity'):
                raise forms.ValidationError('If abnormal, please specify.')
        else:
            if cleaned_data.get('abnormal_activity'):
                raise forms.ValidationError(
                    'You indicated that there was NO abnormality in general activity, yet '
                    'specified abnormality. Please correct')

    def validate_heent_exam(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('heent_exam') == YES:
            if cleaned_data.get('heent_no_other'):
                raise forms.ValidationError(
                    'If HEENT Exam is normal, Do not answer the following Question (Q10).')
        elif cleaned_data.get('heent_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('heent_no_other'):
                raise forms.ValidationError(
                    'You indicated that HEENT exam was not normal. Provide answer to Q10.')

    def validate_resp_exam(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('resp_exam') == YES:
            if cleaned_data.get('resp_exam_other'):
                raise forms.ValidationError(
                    'If Respiratory Exam is normal, Do not answer the following Question (Q12).')
        elif cleaned_data.get('resp_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('resp_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Respiratory exam was not normal. Provide answer to Q12.')

    def validate_cardiac_exam(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('cardiac_exam') == YES:
            if cleaned_data.get('cardiac_exam_other'):
                raise forms.ValidationError(
                    'If Cardiac Exam is normal, Do not answer the following Question (Q14).')
        elif cleaned_data.get('cardiac_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('cardiac_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Cardiac exam was not normal. Provide answer to Q14.')

    def validate_abdominal_exam(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('abdominal_exam') == YES:
            if cleaned_data.get('abdominal_exam_other'):
                raise forms.ValidationError(
                    'If Abdominal Exam is normal, Do not answer the following Question (Q16).')
        elif cleaned_data.get('abdominal_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('abdominal_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Abdominal exam was not normal. Provide answer to Q16.')

    def validate_skin_exam(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('skin_exam') == YES:
            if cleaned_data.get('skin_exam_other'):
                raise forms.ValidationError(
                    'If Skin Exam is normal, Do not answer the following Question (Q18).')
        elif cleaned_data.get('skin_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('skin_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Skin exam was not normal. Provide answer to Q18.')

    def validate_neuro_exam(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('neurologic_exam') == YES:
            if cleaned_data.get('neuro_exam_other'):
                raise forms.ValidationError(
                    'If Neurological Exam is normal, Do not answer the following Question (Q22).')
        elif cleaned_data.get('neurologic_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('neuro_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Neurological exam was not normal. Provide answer to Q22.')

    class Meta:
        model = InfantFuPhysical
        fields = '__all__'
