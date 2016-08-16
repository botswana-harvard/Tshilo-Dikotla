from edc_death_report.forms import DeathReportFormMixin

from ..models import MaternalDeathReport

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalDeathReportForm(DeathReportFormMixin, BaseMaternalModelForm):

    class Meta:
        model = MaternalDeathReport
        fields = '__all__'
