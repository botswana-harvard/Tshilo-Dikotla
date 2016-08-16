from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_base.form.old_forms import BaseModelForm
from edc_constants.constants import ON_STUDY, MISSED_VISIT
from edc_visit_tracking.forms import VisitFormMixin

from tshilo_dikotla.choices import VISIT_REASON, VISIT_INFO_SOURCE, MATERNAL_VISIT_STUDY_STATUS

from ..models import MaternalVisit, MaternalUltraSoundInitial


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
        self.check_creation_of_antenatal_visit_2(cleaned_data)

        return cleaned_data

    def check_creation_of_antenatal_visit_2(self, cleaned_data):
        appointment = cleaned_data.get('appointment')
        gestational_age = MaternalUltraSoundInitial.objects.get(
            maternal_visit__appointment__registered_subject=appointment.registered_subject).ga_confirmed
        if appointment.visit_definition.code == '1020M' and gestational_age < 32:
            raise forms.ValidationError('Antenatal Visit 2 cannot occur before 32 weeks. Current GA is "{}" weeks'.
                                        format(gestational_age))

    class Meta:
        model = MaternalVisit
        fields = '__all__'
