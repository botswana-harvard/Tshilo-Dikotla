from dateutil.relativedelta import relativedelta
from django import forms

from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS

from ..models import MaternalLabourDel, MaternalHivInterimHx

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalLabourDelForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalLabourDelForm, self).clean()
#         if cleaned_data.get('live_infants_to_register') > 1:
#             raise forms.ValidationError("Only one infant per mother can be registered to the study.")
#         if cleaned_data.get('live_infants_to_register') <= 0:
#             raise forms.ValidationError('Number of live infants to register may not be less than or equal to 0!.')
#         if cleaned_data.get('delivery_datetime') > cleaned_data.get('report_datetime'):
#                 raise forms.ValidationError('Delivery date cannot be greater than the report date. '
#                                             'Please correct.')
#         postnatal_enrollment = PostnatalEnrollment.objects.get(
#             registered_subject__subject_identifier=cleaned_data.get(
#                 'maternal_visit').appointment.registered_subject.subject_identifier)
#         expected_delivery_date = cleaned_data.get(
#             'report_datetime').date() - relativedelta(days=postnatal_enrollment.postpartum_days)
#         if cleaned_data.get('delivery_datetime').date() != expected_delivery_date:
#             raise forms.ValidationError(
#                 'Delivery date does not correspond with the number of days post-partum as '
#                 'reported at Postnatal Enrollment. Using \'{}\' days post-partum. Please correct'.format(
#                     postnatal_enrollment.postpartum_days))
#         if cleaned_data.get('has_temp') == YES:
#             if not cleaned_data.get('labour_max_temp'):
#                 raise forms.ValidationError(
#                     'You have indicated that maximum temperature at delivery is known. '
#                     'Please provide the maximum temperature.')
#         else:
#             if cleaned_data.get('labour_max_temp'):
#                 raise forms.ValidationError('You have indicated that maximum temperature is not known. '
#                                             'You CANNOT provide the maximum temperature')
#         if cleaned_data.get('has_vl') == NO and cleaned_data.get('vl_detectable') != NOT_APPLICABLE:
#             raise forms.ValidationError(
#                 'If Viral Load was not performed then Viral Load detectable is Not Applicable.')
        return cleaned_data

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
