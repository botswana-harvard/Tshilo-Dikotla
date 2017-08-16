from django.contrib import admin

from ..forms import InfantBirthDataForm
from ..models import InfantBirthData

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantBirthDataAdmin(BaseInfantScheduleModelAdmin):

    form = InfantBirthDataForm

    fields = (
        "infant_visit",
        "weight_kg",
        "infant_length",
        "head_circumference",
        "apgar_score",
        "apgar_score_min_1",
        "apgar_score_min_5",
        "apgar_score_min_10",
        "congenital_anomalities",
        "other_birth_info")

    radio_fields = {
        "apgar_score": admin.VERTICAL,
        "congenital_anomalities": admin.VERTICAL}

admin.site.register(InfantBirthData, InfantBirthDataAdmin)
