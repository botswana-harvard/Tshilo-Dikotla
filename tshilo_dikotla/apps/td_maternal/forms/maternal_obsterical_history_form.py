from django import forms
from .base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalObstericalHistory


class MaternalObstericalHistoryForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalObstericalHistoryForm, self).clean()
        #self.validate_previous_pregnancies()
        #self.validate_24wks_or_more_pregnancy()
        return cleaned_data

    def validate_previous_pregnancies(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('prev_pregnancies') == 0:
            if (
                cleaned_data.get('pregs_24wks_or_more') != 0 or
                cleaned_data.get('lost_before_24wks') != 0 or
                cleaned_data.get('lost_after_24wks') != 0
            ):
                raise forms.ValidationError('You indicated previous pregancies were 0. '
                                            'Number of pregnancies at or after 24 weeks,'
                                            'number of living children,'
                                            'number of children died after 5 year be greater than all be zero.'
                                            .format(cleaned_data.get('prev_pregnancies')))

        if cleaned_data.get('prev_pregnancies') > 0:
            if (
                cleaned_data.get('pregs_24wks_or_more') == 0 and
                cleaned_data.get('lost_before_24wks') == 0 and
                cleaned_data.get('lost_after_24wks') == 0
            ):
                raise forms.ValidationError('You indicated previous pregancies were {}. '
                                            'Number of pregnancies at or after 24 weeks,'
                                            'number of living children,'
                                            'number of children died after 5 year CANNOT all be zero.'
                                            .format(cleaned_data.get('prev_pregnancies')))

    def validate_24wks_or_more_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('pregs_24wks_or_more') > 0:
            if (
                cleaned_data.get('lost_after_24wks') == 0 and
                cleaned_data.get('live_children') == 0 and
                cleaned_data.get('children_died_b4_5yrs') == 0
            ):
                raise forms.ValidationError('You indicated previous at least 24 weeks were {}. '
                                            'Number of pregnancies least 24 weeks,'
                                            'number of pregnancies lost before 24 weeks,'
                                            'number of pregnancies lost at or after 24 weeks.'
                                            .format(cleaned_data.get('pregs_24wks_or_more')))

        if cleaned_data.get('pregs_24wks_or_more') > cleaned_data.get('prev_pregnancies'):
            raise forms.ValidationError(
                'Number of pregnancies carried at least 24 weeks cannot be greater than previous pregnancies.')
        if cleaned_data.get('lost_before_24wks') > cleaned_data.get('prev_pregnancies'):
            raise forms.ValidationError(
                'Number of pregnancies lost before 24 weeks cannot be greater than previous pregnancies.')
        if (cleaned_data.get('lost_after_24wks') > cleaned_data.get('prev_pregnancies') or
                cleaned_data.get('lost_after_24wks') > cleaned_data.get('pregs_24wks_or_more')):
            raise forms.ValidationError(
                'Number of pregnancies lost at or after 24 weeks gestation '
                'cannot be greater than number of previous pregnancies or number of pregnancies at least 24 weeks.')
        if (cleaned_data.get('pregs_24wks_or_more') +
                cleaned_data.get('lost_before_24wks')) != cleaned_data.get('prev_pregnancies'):
            raise forms.ValidationError(
                'The sum of Number of pregnancies at least 24 weeks and '
                'number of pregnancies lost before 24 weeks gestation. must be equal to '
                'number of previous pregnancies for this participant.')

    class Meta:
        model = MaternalObstericalHistory
        fields = '__all__'
