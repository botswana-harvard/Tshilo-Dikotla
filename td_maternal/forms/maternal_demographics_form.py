from ..models import MaternalDemographics

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalDemographicsForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalDemographics
        fields = '__all__'
