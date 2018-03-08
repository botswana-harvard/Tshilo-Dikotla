from django import forms
from django.db import models

from django.conf import settings
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE
from lab_requisition.forms import RequisitionFormMixin

from tshilo_dikotla.choices import STUDY_SITES, REASON_NOT_DRAWN
# from tshilo_dikotla.td_infant.models import InfantStoolCollection

from ..models import InfantRequisition


class InfantRequisitionForm(RequisitionFormMixin):

    study_site = forms.ChoiceField(
        label='Study site',
        choices=STUDY_SITES,
        initial=settings.DEFAULT_STUDY_SITE,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def __init__(self, *args, **kwargs):
        super(InfantRequisitionForm, self).__init__(*args, **kwargs)
        self.fields['item_type'].initial = 'tube'

    def clean(self):
        cleaned_data = super(InfantRequisitionForm, self).clean()
        self.validate_drawing_requisitions(cleaned_data)
#         self.validate_sample_swabs()
#         self.validate_dna_pcr_and_cytokines()
#         self.validate_stool_sample_collection()
#         self.validate_requisition_and_infant_visit()
        return cleaned_data

    def validate_requisition_and_drawn_datetime(self, cleaned_data):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('drawn_datetime'):
            if cleaned_data.get('drawn_datetime').date() < cleaned_data.get('requisition_datetime').date():
                raise forms.ValidationError(
                    'Requisition date cannot be in future of specimen date. Specimen draw date is '
                    'indicated as {}, whilst requisition is indicated as{}. Please correct'.format(
                        cleaned_data.get('drawn_datetime').date(),
                        cleaned_data.get('requisition_datetime').date()))

    def validate_drawing_requisitions(self, cleaned_data):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('is_drawn') == YES and not cleaned_data.get('drawn_datetime'):
            raise forms.ValidationError("A specimen was collected. Please provide the date and time collected.")

        if cleaned_data.get('is_drawn') == NO and cleaned_data.get('drawn_datetime'):
            raise forms.ValidationError("A specimen was not collected, date and time collected NA.")

        if cleaned_data.get('is_drawn') == NO and not cleaned_data.get('reason_not_drawn'):
            raise forms.ValidationError("Please provide a reason why the specimen was not collected.")

        if cleaned_data.get('is_drawn') == YES and cleaned_data.get('reason_not_drawn_other'):
            raise forms.ValidationError(
                "A specimen was drawn. Do not provided a reason why it was not collected.")

        if cleaned_data.get('reason_not_drawn') == OTHER and not cleaned_data.get('reason_not_drawn_other'):
            raise forms.ValidationError(
                "Please specify Other reason why specimen was not drawn.")

    def validate_sample_swabs(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('panel').name == 'Rectal swab (Storage)':
            if cleaned_data.get('item_type') != 'swab':
                raise forms.ValidationError('Panel {} is a swab therefore collection type is swab. Please correct.'
                                            .format(cleaned_data.get('panel').name))

    def validate_dna_pcr_and_cytokines(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('panel').name in ['DNA PCR', 'Inflammatory Cytokines']:
            if cleaned_data.get('item_type') not in ['dbs', 'tube']:
                raise forms.ValidationError('Panel {} collection type can only be dbs or tube. '
                                            'Please correct.'.format(cleaned_data.get('panel').name))

#     def validate_stool_sample_collection(self):
#         cleaned_data = self.cleaned_data
#         sample_collection = InfantStoolCollection.objects.filter(infant_visit=cleaned_data.get('infant_visit'))
#         if sample_collection:
#             sample_collection = InfantStoolCollection.objects.get(infant_visit=cleaned_data.get('infant_visit'))
#             if sample_collection.sample_obtained == YES:
#                 if (cleaned_data.get("panel").name == 'Stool storage' and cleaned_data.get("is_drawn") == NO):
#                     raise forms.ValidationError("Stool Sample Collected. Stool Requisition is_drawn"
#                                                 " cannot be NO.")

    def validate_requisition_and_infant_visit(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('infant_visit').is_present == YES and
                cleaned_data.get('reason_not_drawn') == 'absent'):
            raise forms.ValidationError(
                'Reason not drawn cannot be absent. On the visit report you said infant is present.'
                ' Please Correct.')

    class Meta:
        model = InfantRequisition
        fields = '__all__'
