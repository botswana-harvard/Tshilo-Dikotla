from ..models import MaternalPostPartumDep
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalPostPartumDepForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalPostPartumDepForm, self).clean()
        return cleaned_data

    class Meta:
        model = MaternalPostPartumDep
        fields = '__all__'
