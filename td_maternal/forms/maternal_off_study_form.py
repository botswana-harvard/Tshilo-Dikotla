from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_offstudy.forms import OffStudyFormMixin

from tshilo_dikotla.choices import OFF_STUDY_REASON

from ..models import MaternalOffStudy, MaternalConsent

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalOffStudyForm (OffStudyFormMixin, BaseMaternalModelForm):

    reason = forms.ChoiceField(
        label='Please code the primary reason participant taken off-study',
        choices=[choice for choice in OFF_STUDY_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        cleaned_data = super(MaternalOffStudyForm, self).clean()
        self.validate_offstudy_date()
        return cleaned_data

    def validate_offstudy_date(self):
        cleaned_data = self.cleaned_data
        subject_identifier = cleaned_data.get(
            'maternal_visit').appointment.registered_subject.subject_identifier
        consent = MaternalConsent.objects.filter(
            maternal_eligibiliry__registered_subject__subject_identifier=subject_identifier).order_by('consent_datetime').first()
        if consent:
            if cleaned_data.get('offstudy_date') < consent.consent_datetime.date():
                raise forms.ValidationError(
                    "Off study date cannot be before consent date")
            if cleaned_data.get('offstudy_date') < consent.dob:
                raise forms.ValidationError(
                    "Off study date cannot be before dob")
        else:
            raise forms.ValidationError('Maternal Consent does not exist.')

    class Meta:
        model = MaternalOffStudy
        fields = '__all__'
