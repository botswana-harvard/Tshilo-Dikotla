from dateutil.relativedelta import relativedelta
from django import forms

from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS

from ..models import MaternalLabourDel, MaternalHivInterimHx, MaternalVisit
from ..classes import MaternalStatusHelper

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalLabourDelForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalLabourDelForm, self).clean()
        self.validate_valid_regimen_hiv_pos_only()
        return cleaned_data

    def validate_valid_regimen_hiv_pos_only(self):
        cleaned_data = self.cleaned_data
        registered_subject = cleaned_data.get('registered_subject')
        latest_visit = MaternalVisit.objects.filter(subject_identifier=registered_subject.subject_identifier).order_by('-created').first()
        maternal_status_helper = MaternalStatusHelper(latest_visit)
        if maternal_status_helper.hiv_status == POS:
            if cleaned_data.get('valid_regiment_duration') not in YES:
                raise forms.ValidationError('Participant is HIV+ valid regimen duration should be YES. Please correct.')
            if cleaned_data.get('valid_regiment_duration') == YES and not cleaned_data.get('arv_initiation_date'): 
                raise forms.ValidationError('You indicated participant was on valid regimen, please give a valid arv initiation date.')
            if (cleaned_data.get('valid_regiment_duration') == YES and
            (cleaned_data.get('delivery_datetime').date() - relativedelta(weeks=4) <
             cleaned_data.get('arv_initiation_date'))):
                raise forms.ValidationError('You indicated that the mother was on REGIMEN for a valid duration, but'
                                            ' delivery date is within 4weeks of art initiation date. Please correct.')
        else:
            if cleaned_data.get('valid_regiment_duration') not in [NOT_APPLICABLE]:
                raise forms.ValidationError('Participant\'s HIV status is {}, valid regimen duration should be Not Applicable.'.format(maternal_status_helper.hiv_status))
            if cleaned_data.get('arv_initiation_date'):
                raise forms.ValidationError('Participant\'s HIV status is {}, arv initiation date should not filled.'.format(maternal_status_helper.hiv_status))

    class Meta:
        model = MaternalLabourDel
        fields = '__all__'


class MaternalHivInterimHxForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalHivInterimHxForm, self).clean()
#         self.validate_cd4()
#         self.validate_viral_load()
#         self.validate_vl_result()
        return cleaned_data

    def validate_cd4(self):
        # If CD4 performed, date and result should be supplied
        cleaned_data = self.cleaned_data
        if cleaned_data.get('has_cd4') == YES:
            if not cleaned_data.get('cd4_date'):
                raise forms.ValidationError(
                    'You indicated that a CD4 count was performed. Please provide the date.')
            if not cleaned_data.get('cd4_result'):
                raise forms.ValidationError(
                    'You indicated that a CD4 count was performed. Please provide the result.')
        else:
            # If cd4 was not performed no date nor result should be provided
            if cleaned_data.get('cd4_date'):
                raise forms.ValidationError(
                    'You indicated that a CD4 count was NOT performed, yet provided a date '
                    'CD4 was performed. Please correct.')
            if cleaned_data.get('cd4_result'):
                raise forms.ValidationError(
                    'You indicated that a CD4 count was NOT performed, yet provided a CD4 '
                    'result. Please correct.')

    def validate_viral_load(self):
        # If VL performed, date and result should be supplied
        cleaned_data = self.cleaned_data
        if cleaned_data.get('has_vl') == YES:
            if not cleaned_data.get('vl_date'):
                raise forms.ValidationError(
                    'You indicated that a VL count was performed. Please provide the date.')
            if cleaned_data.get('vl_detectable') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You stated that a VL count was performed. Please indicate if it '
                    'was detectable.')
        else:
            # If VL was not performed, no VL date nor result should be supplied
            if cleaned_data.get('vl_date'):
                raise forms.ValidationError(
                    'You indicated that a VL count was NOT performed, yet provided a date VL '
                    'was performed. Please correct.')
            if cleaned_data.get('vl_result'):
                raise forms.ValidationError(
                    'You indicated that a VL count was NOT performed, yet provided a VL result'
                    ' Please correct.')
            if cleaned_data.get('vl_detectable') != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You stated that a VL count was NOT performed, you CANNOT indicate if VL '
                    'was detectable.')

    def validate_vl_result(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('vl_detectable') == YES:
            if not cleaned_data.get('vl_result'):
                raise forms.ValidationError(
                    'You indicated that the VL was detectable. Provide provide VL result.')
        else:
            if cleaned_data.get('vl_result'):
                raise forms.ValidationError(
                    'You indicated that the VL was NOT detectable. you cannot provide a result.')

    class Meta:
        model = MaternalHivInterimHx
        fields = '__all__'
