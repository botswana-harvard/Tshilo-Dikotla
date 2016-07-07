from edc_death_report.forms import DeathReportFormMixin

from ..models import InfantDeathReport

from .base_infant_model_form import BaseInfantModelForm


class InfantDeathReportForm(DeathReportFormMixin, BaseInfantModelForm):

    class Meta:
        model = InfantDeathReport
        fields = '__all__'
