from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_base.form.old_forms import BaseModelForm
from edc_constants.constants import ON_STUDY, MISSED_VISIT
from edc_visit_tracking.forms import VisitFormMixin

from tshilo_dikotla.choices import VISIT_REASON, VISIT_INFO_SOURCE, MATERNAL_VISIT_STUDY_STATUS, INFO_PROVIDER

from ..models import MaternalVisit, MaternalConsent


class MaternalVisitForm (VisitFormMixin, BaseModelForm):

    participant_label = 'mother'

    study_status = forms.ChoiceField(
        label='What is the mother\'s current study status',
        choices=MATERNAL_VISIT_STUDY_STATUS,
        initial=ON_STUDY,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    info_source = forms.ChoiceField(
        label='Source of information',
        required=False,
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        cleaned_data = super(MaternalVisitForm, self).clean()
        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = MaternalVisit(**self.cleaned_data)
        instance.subject_failed_eligibility(forms.ValidationError)

        return cleaned_data

    class Meta:
        model = MaternalVisit
        fields = '__all__'
