from django import forms

from ..models import MaternalInterimIdcc

from edc_constants.constants import YES, NO

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalInterimIdccForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalInterimIdccForm, self).clean()
        self.validate_info_since_last_visit_yes()
        self.validate_info_since_last_visit_no()
        return cleaned_data

    def validate_info_since_last_visit_yes(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('info_since_lastvisit') == YES:
#TODO: validate when value_vl_size is none and value_vl is not answered
            if cleaned_data.get('recent_cd4'):
                if not cleaned_data.get('recent_cd4_date'):
                    raise forms.ValidationError('You specified that there is recent cd4 information available,'
                                                ' please provide the date')

            if cleaned_data.get('recent_cd4_date') and not cleaned_data.get('recent_cd4'):
                raise forms.ValidationError('You provided the date for the CD4 information but have not'
                                            ' indicated the CD4 value')

            if cleaned_data.get('value_vl'):
                if not cleaned_data.get('recent_vl_date'):
                    raise forms.ValidationError('You indicated that there was a VL value, please provide the'
                                                ' date it was determined')

            if cleaned_data.get('value_vl_size') == 'less_than' and cleaned_data.get('value_vl') != 400:
                raise forms.ValidationError('You indicated that the value of the most recent VL is less_than a number,'
                                            ' therefore the value of VL should be 400')

            if cleaned_data.get('value_vl_size') == 'greater_than' and cleaned_data.get('value_vl') != 750000:
                raise forms.ValidationError('You indicated that the value of the most recent VL is greater_than a'
                                            ' number, therefore the value of VL should be 750000')

            if(cleaned_data.get('value_vl_size') == 'equal' and (cleaned_data.get('value_vl') > 750000 or
               cleaned_data.get('value_vl') < 400)):
                raise forms.ValidationError('You indicated that the value of the most recent VL is equal to a'
                                            ' number, therefore the value of VL should be between 400 and 750000'
                                            '(inclusive of 400 and 750,000)')

    def validate_info_since_last_visit_no(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('info_since_lastvisit') == NO:
            if(cleaned_data.get('recent_cd4') or cleaned_data.get('recent_cd4_date') or
               cleaned_data.get('value_vl_size') or cleaned_data.get('value_vl') or
               cleaned_data.get('recent_vl_date') or cleaned_data.get('other_diagnoses')):
                raise forms.ValidationError('You indicated that there has not been any lab information since the last visit'
                                            ' please do not answer the questions on CD4, VL and diagnoses found')

    class Meta:
        model = MaternalInterimIdcc
        fields = '__all__'
