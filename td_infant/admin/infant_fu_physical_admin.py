from django.contrib import admin

from ..forms import InfantFuPhysicalForm
from ..models import InfantFuPhysical

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantFuPhysicalAdmin(BaseInfantScheduleModelAdmin):
    form = InfantFuPhysicalForm

    radio_fields = {
        'general_activity': admin.VERTICAL,
        'physical_exam_result': admin.VERTICAL,
        'heent_exam': admin.VERTICAL,
        'resp_exam': admin.VERTICAL,
        'cardiac_exam': admin.VERTICAL,
        'abdominal_exam': admin.VERTICAL,
        'skin_exam': admin.VERTICAL,
        'neurologic_exam': admin.VERTICAL
    }

admin.site.register(InfantFuPhysical, InfantFuPhysicalAdmin)
