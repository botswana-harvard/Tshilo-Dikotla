from django import forms
from .base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalObstericalHistory, MaternalUltraSoundInitial


class MaternalObstericalHistoryForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalObstericalHistoryForm, self).clean()
        self.validate_less_than_24_weeks_pregnant()
        self.validate_24wks_or_more_pregnancy()
        self.validate_live_children()
        return cleaned_data

    def validate_less_than_24_weeks_pregnant(self):
        cleaned_data = self.cleaned_data
        ultrasound = self.check_mother_gestational_age()
        if not ultrasound:
            raise forms.ValidationError('Please complete the Ultrasound form first.')
        else:
            if cleaned_data.get('prev_pregnancies') == 1 and ultrasound[0].ga_confirmed < 24:
                if (
                    cleaned_data.get('pregs_24wks_or_more') != 0 or
                    cleaned_data.get('lost_before_24wks') != 0 or
                    cleaned_data.get('lost_after_24wks') != 0
                ):
                    raise forms.ValidationError('You indicated previous pregancies were {}. '
                                                'Number of pregnancies at or after 24 weeks, '
                                                'number of living children, '
                                                'number of children lost after 24 weeks should all be zero.'
                                                .format(cleaned_data.get('prev_pregnancies')))

            if cleaned_data.get('prev_pregnancies') > 1 and ultrasound[0].ga_confirmed < 24:
                sum_pregnancies = (
                    cleaned_data.get('pregs_24wks_or_more') +
                    cleaned_data.get('lost_before_24wks') +
                    cleaned_data.get('lost_after_24wks'))
                if sum_pregnancies != (cleaned_data.get('prev_pregnancies') - 1):
                    raise forms.ValidationError('The sum of Q3, Q4 and Q5 must all add up to Q2 - 1. Please correct.')

    def validate_24wks_or_more_pregnancy(self):
        cleaned_data = self.cleaned_data
        ultrasound = self.check_mother_gestational_age()
        if not ultrasound:
            raise forms.ValidationError('Please complete the Ultrasound form first.')
        else:
            if cleaned_data.get('prev_pregnancies') > 0 and ultrasound[0].ga_confirmed >= 24:
                sum_pregnancies = (
                    cleaned_data.get('pregs_24wks_or_more') +
                    cleaned_data.get('lost_before_24wks') +
                    cleaned_data.get('lost_after_24wks'))
                if sum_pregnancies != cleaned_data.get('prev_pregnancies'):
                    raise forms.ValidationError('The sum of Q3, Q4 and Q5 must be equal to Q2. Please correct.')

    def validate_live_children(self):
        cleaned_data = self.cleaned_data
        sum_deliv_37_wks = cleaned_data.get('children_deliv_before_37wks') + cleaned_data.get('children_deliv_aftr_37wks')
        sum_lost_24_wks = cleaned_data.get('lost_before_24wks') + cleaned_data.get('lost_after_24wks')
        if sum_deliv_37_wks != ((cleaned_data.get('prev_pregnancies') - 1) - sum_lost_24_wks):
            raise forms.ValidationError('The sum of Q8 and Q9 must be equal to (Q2 -1) - (Q4 + Q5). Please correct.')

    def check_mother_gestational_age(self):
        cleaned_data = self.cleaned_data
        maternal_visit = cleaned_data.get('maternal_visit')
        return MaternalUltraSoundInitial.objects.filter(maternal_visit=maternal_visit)

    class Meta:
        model = MaternalObstericalHistory
        fields = '__all__'
