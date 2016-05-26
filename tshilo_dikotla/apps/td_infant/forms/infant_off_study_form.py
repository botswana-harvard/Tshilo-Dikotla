from django import forms
from django.contrib.admin.widgets import (AdminRadioSelect,
                                          AdminRadioFieldRenderer)

from tshilo_dikotla.apps.td_maternal.models import MaternalConsent

from ..choices import OFF_STUDY_REASON

from ..forms import BaseInfantModelForm
from ..models import InfantOffStudy


class InfantOffStudyForm(BaseInfantModelForm):

    reason = forms.ChoiceField(
        label='Please code the primary reason participant taken off-study',
        choices=[choice for choice in OFF_STUDY_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    class Meta:
        model = InfantOffStudy
        fields = '__all__'

    def clean(self):
        cleaned_data = super(InfantOffStudyForm, self).clean()
#         self.validate_offstudy_date()
        return cleaned_data

    def validate_offstudy_date(self):
        cleaned_data = self.cleaned_data
        maternal_subject_identifier = cleaned_data.get(
            'infant_visit').appointment.registered_subject.relative_identifier
        maternal_consent = MaternalConsent.objects.get(
            registered_subject__subject_identifier=maternal_subject_identifier)
        if cleaned_data.get('offstudy_date') < maternal_consent.consent_datetime.date():
            raise forms.ValidationError(
                'Off study date cannot be before consent date')
        if cleaned_data.get('offstudy_date') < maternal_consent.dob:
            raise forms.ValidationError(
                'Off study date cannot be before date of birth')
