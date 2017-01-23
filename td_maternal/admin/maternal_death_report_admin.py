from django.contrib import admin

from ..forms import MaternalDeathReportForm
from ..models import MaternalDeathReport

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalDeathReportAdmin(BaseMaternalModelAdmin):

    form = MaternalDeathReportForm
    fields = (
        "maternal_visit",
        "report_datetime",
        "death_date",
        "cause",
        "cause_other",
        "perform_autopsy",
        "death_cause",
        "cause_category",
        "cause_category_other",
        "diagnosis_code",
        "diagnosis_code_other",
        "illness_duration",
        "medical_responsibility",
        "participant_hospitalized",
        "reason_hospitalized",
        "reason_hospitalized_other",
        "days_hospitalized",
        "comment")
    radio_fields = {
        "perform_autopsy": admin.VERTICAL,
        "participant_hospitalized": admin.VERTICAL,
    }
    filter_horizontal = ('cause', 'cause_category', 'diagnosis_code', 'reason_hospitalized', 'medical_responsibility')

admin.site.register(MaternalDeathReport, MaternalDeathReportAdmin)
