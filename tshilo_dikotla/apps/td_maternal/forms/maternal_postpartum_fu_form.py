from ..models import MaternalPostPartumFu
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalPostPartumFuForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalPostPartumFuForm, self).clean()
        return cleaned_data

    class Meta:
        model = MaternalPostPartumFu
        fields = '__all__'
