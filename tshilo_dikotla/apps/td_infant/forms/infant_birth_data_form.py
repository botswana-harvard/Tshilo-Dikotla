from django import forms

from edc_constants.constants import YES

from ..models import InfantBirthData

from .base_infant_model_form import BaseInfantModelForm


class InfantBirthDataForm(BaseInfantModelForm):

    class Meta:
        model = InfantBirthData
        fields = '__all__'

    def clean(self):
        cleaned_data = super(InfantBirthDataForm, self).clean()
#         self.validate_apgar_score(cleaned_data)
        return cleaned_data

    def validate_apgar_score(self, cleaned_data):
        if cleaned_data.get('apgar_score') == YES:
            if not cleaned_data.get('apgar_score_min_1') == 0:
                if not cleaned_data.get('apgar_score_min_1'):
                    raise forms.ValidationError('If Apgar scored performed, then you should answer At 1 minute(Q7).')
            if not cleaned_data.get('apgar_score_min_5') == 0:
                if not cleaned_data.get('apgar_score_min_5'):
                    raise forms.ValidationError('If Apgar scored performed, then you should answer At 5 minute(Q8).')
        else:
            if cleaned_data.get('apgar_score_min_1'):
                raise forms.ValidationError('If Apgar scored was NOT performed, then you should NOT answer at '
                                            '1 minute(Q7).')
            if cleaned_data.get('apgar_score_min_5'):
                raise forms.ValidationError('If Apgar scored was NOT performed, then you should NOT answer at 5 '
                                            'minute(Q8).')
            if cleaned_data.get('apgar_score_min_10'):
                raise forms.ValidationError('If Apgar scored was NOT performed, then you should NOT answer at 10 '
                                            'minute(Q9).')
