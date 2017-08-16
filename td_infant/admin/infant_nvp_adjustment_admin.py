from django.contrib import admin

from ..forms import InfantNvpAdjustmentForm
from ..models import InfantNvpAdjustment

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantNvpAdjustmentAdmin(BaseInfantScheduleModelAdmin, admin.ModelAdmin):

    form = InfantNvpAdjustmentForm

    radio_fields = {
        'dose_adjustment': admin.VERTICAL,
        'dose_4_weeks': admin.VERTICAL}

    list_display = ('infant_visit', 'dose_adjustment', 'dose_4_weeks',)

    list_filter = ('dose_adjustment', 'dose_4_weeks',)

admin.site.register(InfantNvpAdjustment, InfantNvpAdjustmentAdmin)
