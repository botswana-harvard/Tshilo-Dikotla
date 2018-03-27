from edc_constants.constants import SCHEDULED, UNSCHEDULED, NO, YES, OTHER
from lab_requisition.forms import RequisitionFormMixin

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from td_maternal.models import MaternalVisit
from tshilo_dikotla.choices import STUDY_SITES

from ..models import MaternalRequisition


class MaternalRequisitionForm(RequisitionFormMixin):

    study_site = forms.ChoiceField(
        label='Study site',
        choices=STUDY_SITES,
        initial=settings.DEFAULT_STUDY_SITE,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def __init__(self, *args, **kwargs):
        super(MaternalRequisitionForm, self).__init__(*args, **kwargs)
        self.fields['item_type'].initial = 'tube'

    def clean(self):
        cleaned_data = super(MaternalRequisitionForm, self).clean()
        self.validate_drawing_requisitions(cleaned_data)
        self.validate_requisition_and_drawn_datetime()
        return cleaned_data

    def validate_drawing_requisitions(self, cleaned_data):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('is_drawn') == YES and not cleaned_data.get('drawn_datetime'):
            raise forms.ValidationError("A specimen was collected. Please provide the date and time collected.")

        if cleaned_data.get('is_drawn') == NO and cleaned_data.get('drawn_datetime'):
            raise forms.ValidationError("A specimen was not collected, date and time collected NA.")

        if cleaned_data.get('is_drawn') == NO and not cleaned_data.get('reason_not_drawn'):
            raise forms.ValidationError("Please provide a reason why the specimen was not collected.")

        if cleaned_data.get('is_drawn') == YES and cleaned_data.get('reason_not_drawn'):
            raise forms.ValidationError(
                "A specimen was not drawn. Do not provided a reason why it was not collected.")

        if cleaned_data.get('is_drawn') == YES and cleaned_data.get('reason_not_drawn_other'):
            raise forms.ValidationError(
                "A specimen was drawn. Do not provided a reason why it was not collected.")

        if cleaned_data.get('reason_not_drawn') == 'other' and not cleaned_data.get('reason_not_drawn_other'):
            raise forms.ValidationError(
                "Please specify Other reason why requisition was not drawn.")

    def validate_requisition_and_drawn_datetime(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('drawn_datetime'):
            if cleaned_data.get('drawn_datetime').date() < cleaned_data.get('requisition_datetime').date():
                raise forms.ValidationError(
                    'Requisition date cannot be in future of specimen date. Specimen draw date is '
                    'indicated as {}, whilst requisition is indicated as{}. Please correct'.format(
                        cleaned_data.get('drawn_datetime').date(),
                        cleaned_data.get('requisition_datetime').date()))

        if (
            cleaned_data.get('panel').name == 'Vaginal swab (Storage)' or
            cleaned_data.get('panel').name == 'Rectal swab (Storage)' or
            cleaned_data.get('panel').name == 'Skin Swab (Storage)' or
            cleaned_data.get('panel').name == 'Vaginal STI Swab (Storage)'
        ):
            if cleaned_data.get('item_type') != 'swab':
                raise forms.ValidationError(
                    'Panel is a swab therefore collection type is swab. Please correct.')
        else:
            if cleaned_data.get('item_type') != 'tube':
                raise forms.ValidationError('Panel {} can only be tube therefore collection type is swab. '
                                            'Please correct.'.format(cleaned_data.get('panel').name))
        maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=cleaned_data.get(
                'maternal_visit').appointment.registered_subject,
            appointment=cleaned_data.get('maternal_visit').appointment,
            appointment__visit_instance=cleaned_data.get('maternal_visit').appointment.visit_instance)
        if maternal_visit:
            if ((maternal_visit.reason == SCHEDULED or maternal_visit.reason == UNSCHEDULED) and
                    cleaned_data.get('reason_not_drawn') == 'absent'):
                raise forms.ValidationError(
                    'Reason not drawn cannot be {}. Visit report reason is {}'.format(
                        cleaned_data.get('reason_not_drawn'),
                        maternal_visit.reason))

        return cleaned_data

    class Meta:
        model = MaternalRequisition
        fields = '__all__'
