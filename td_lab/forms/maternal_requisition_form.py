from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED
from edc_lab.requisition.forms import RequisitionFormMixin

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
        print(cleaned_data, "cleaned_data, cleaned_data, cleaned_data, cleaned_data")
        if cleaned_data.get('drawn_datetime'):
            if cleaned_data.get('drawn_datetime').date() < cleaned_data.get('requisition_datetime').date():
                raise forms.ValidationError(
                    'Requisition date cannot be in future of specimen date. Specimen draw date is '
                    'indicated as {}, whilst requisition is indicated as{}. Please correct'.format(
                        cleaned_data.get('drawn_datetime').date(),
                        cleaned_data.get('requisition_datetime').date()))
        if (
            cleaned_data.get('panel_name') == 'Vaginal swab (Storage)' or
            cleaned_data.get('panel_name') == 'Rectal swab (Storage)' or
            cleaned_data.get('panel_name') == 'Skin Swab (Storage)' or
            cleaned_data.get('panel_name') == 'Vaginal STI Swab (Storage)'
        ):
            if cleaned_data.get('item_type') != 'swab':
                raise forms.ValidationError('Panel is a swab therefore collection type is swab. Please correct.')
        else:
            if cleaned_data.get('item_type') != 'tube':
                raise forms.ValidationError('Panel {} can only be tube therefore collection type is swab. '
                                            'Please correct.'.format(cleaned_data.get('panel').name))
#         maternal_visit = MaternalVisit.objects.get(
# #             appointment__registered_subject=cleaned_data.get('maternal_visit').appointment.registered_subject,
#             appointment=cleaned_data.get('maternal_visit').appointment,
#             appointment__visit_instance=cleaned_data.get('maternal_visit').appointment.visit_instance)
        maternal_visit = cleaned_data.get('maternal_visit')
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
