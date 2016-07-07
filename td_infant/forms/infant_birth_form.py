from django import forms

from edc_constants.constants import YES

from edc_base.form.old_forms import BaseModelForm
from td_maternal.models import MaternalLabourDel

from ..models import InfantBirth


class InfantBirthForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(InfantBirthForm, self).clean()
        # DOB should match delivery date
#         maternal_identifier = cleaned_data.get('registered_subject').relative_identifier
#         try:
#             maternal_lab_del = MaternalLabourDel.objects.get(
#                 maternal_visit__appointment__registered_subject__subject_identifier=maternal_identifier)
#             if not cleaned_data.get('dob', None) == maternal_lab_del.delivery_datetime.date():
#                 raise forms.ValidationError('Infant dob must match maternal delivery date of {}. You wrote {}'
#                                             .format(maternal_lab_del.delivery_datetime.date(),
#                                                     cleaned_data.get('dob')))
#             if not self.instance.id:
#                 if InfantBirth.objects.get(maternal_labour_del=maternal_lab_del):
#                     raise forms.ValidationError(
#                         "Infant birth record cannot be saved. An infant has already been "
#                         "registered for this mother.")
#         except MaternalLabourDel.DoesNotExist:
#             raise forms.ValidationError('Cannot find maternal labour and delivery form for this infant!'
#                                         ' This is not expected.')
#         except InfantBirth.DoesNotExist:
#             pass
        return cleaned_data

    class Meta:
        model = InfantBirth
        fields = '__all__'
