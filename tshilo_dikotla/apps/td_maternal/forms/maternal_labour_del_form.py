from dateutil.relativedelta import relativedelta
from django import forms

from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS

from ..models import MaternalLabourDel


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
