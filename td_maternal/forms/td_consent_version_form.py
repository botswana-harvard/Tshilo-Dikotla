from edc_base.form.old_forms import BaseModelForm

from ..models import TdConsentVersion
from django import forms

from td_maternal.models.maternal_off_study import MaternalOffStudy


class TdConsentVersionForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(TdConsentVersionForm, self).clean()
        self.checks_offstudy_status()
        return cleaned_data

    def get_offstudy_instance(self, model_class):
        cleaned_data = self.cleaned_data
        try:
            model_class.objects.get(maternal_visit__subject_identifier=cleaned_data.get(
                'maternal_eligibility').registered_subject.subject_identifier)
        except model_class.DoesNotExist:
            pass
        else:
            raise forms.ValidationError('Participant has been put offstudy, '
                                             'Cannot be re-consented to V3')

    def checks_offstudy_status(self):
        self.get_offstudy_instance(MaternalOffStudy)

    class Meta:
        model = TdConsentVersion
        fields = '__all__'
