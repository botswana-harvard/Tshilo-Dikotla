from django import forms

from edc_constants.constants import NO, YES

from ..models import InfantFuDx, InfantFuDxItems, InfantFu
from ..forms import InfantFuForm
from .base_infant_model_form import BaseInfantModelForm


class InfantFuDxForm(BaseInfantModelForm):

    class Meta:
        model = InfantFuDx
        fields = '__all__'


class InfantFuDxItemsForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantFuDxItemsForm, self).clean()
        self.validate_health_facility()
        self.validate_reported_hospitalization()
        self.validate_other_serious_grade3or4_infection_specification()
        self.validate_other_serious_grade3or4_non_infectious_specification()
        self.validate_other_abnormallaboratory_tests_specification()
        self.validate_new_congenital_abnormality_not_previously_identified_specification()
        return cleaned_data

    def check_infant_hospitalization(self, infant_visit):
        """Check if Question6 on Infant Follow Up form is answered YES"""
        try:
            infant_fu = InfantFu.objects.get(infant_visit=infant_visit)
            return infant_fu.was_hospitalized
        except Exception as e:
            pass

    def validate_reported_hospitalization(self):
        cleaned_data = self.cleaned_data
        infant_visit = cleaned_data.get('infant_fu_dx').infant_visit
        if self.check_infant_hospitalization(infant_visit) == NO:
            raise forms.ValidationError(
                'Question6 in Infant Follow Up is not answered YES, you cannot fill this form.')

    def validate_health_facility(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('health_facility') == NO:
            if cleaned_data.get('was_hospitalized') == YES:
                raise forms.ValidationError(
                    'You indicated that participant was hospitalized, therefore the participant '
                    'was seen at a health facility. Please correct.')

    def validate_other_serious_grade3or4_infection_specification(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('fu_dx') == 'Other serious (grade 3 or 4)infection(not listed above),specify':
            if not cleaned_data.get('fu_dx_specify'):
                raise forms.ValidationError(
                    'You mentioned there is other serious (grade 3 or 4) infection, Please specify')

    def validate_other_serious_grade3or4_non_infectious_specification(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('fu_dx') == 'Other serious (grade 3 or 4) non-infectious(not listed above),specify':
            if not cleaned_data.get('fu_dx_specify'):
                raise forms.ValidationError(
                    'You mentioned there is other serious (grade 3 or 4) non-infectious, Please specify')

    def validate_other_abnormallaboratory_tests_specification(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('fu_dx') == 'Other abnormallaboratory tests(other than tests listed above ''or tests done as part of this study), specify test and result':
            if not cleaned_data.get('fu_dx_specify'):
                raise forms.ValidationError(
                    'You mentioned there is abnormallaboratory tests, Please specify')

    def validate_new_congenital_abnormality_not_previously_identified_specification(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('fu_dx') == 'New congenital abnormality not previously identified?,specify':
            if not cleaned_data.get('fu_dx_specify'):
                raise forms.ValidationError(
                    'You mentioned there is new congenital abnormality not previously identified , Please specify')

    class Meta:
        model = InfantFuDxItems
        fields = '__all__'
