from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_offstudy.forms import OffStudyFormMixin

from tshilo_dikotla.apps.td.choices import OFF_STUDY_REASON

from ..models import MaternalOffStudy

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

    class Meta:
        model = MaternalOffStudy
