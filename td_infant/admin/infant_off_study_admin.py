from django.contrib import admin

from tshilo_dikotla.constants import INFANT

from ..forms import InfantOffStudyForm
from ..models import InfantOffStudy

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantOffStudyAdmin(BaseInfantScheduleModelAdmin):

    form = InfantOffStudyForm
    dashboard_type = INFANT
    visit_model_name = 'infantvisit'

    fields = (
        'infant_visit',
        'report_datetime',
        'offstudy_date',
        'reason',
        'reason_other',
        'comment',
    )

    list_display = (
        'infant_visit',
        'offstudy_date',
        'reason')

admin.site.register(InfantOffStudy, InfantOffStudyAdmin)
