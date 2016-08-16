from edc_locator.forms import LocatorFormMixin

from ..models import MaternalLocator

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalLocatorForm(LocatorFormMixin, BaseMaternalModelForm):

    class Meta:
        model = MaternalLocator
        fields = '__all__'
