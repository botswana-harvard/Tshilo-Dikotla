from django import forms

from ..models import MaternalAztNvp, MaternalRando
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalAztNvpForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalAztNvpForm, self).clean()
        self.validate_randomization(cleaned_data)
        return cleaned_data

    class Meta:
        model = MaternalAztNvp
        fields = '__all__'

    def validate_randomization(self, cleaned_data):
        maternal_randomization = MaternalRando.objects.get(
            subject_identifier=cleaned_data.get('maternal_visit').appointment.registered_subject.subject_identifier)
        if maternal_randomization.rx != cleaned_data.get('azt_nvp'):
            raise forms.ValidationError('The chosen prophylaxis regiment does not match the randomized regiment. '
                                        ' Got {}, while randomization was {}'.format(maternal_randomization.rx,
                                                                                     cleaned_data.get('azt_nvp')))
