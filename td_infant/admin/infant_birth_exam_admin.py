from django.contrib import admin

from ..models import InfantBirthExam
from ..forms import InfantBirthExamForm

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantBirthExamAdmin(BaseInfantScheduleModelAdmin):
    form = InfantBirthExamForm

    list_display = (
        'infant_visit',
        'general_activity',
        'physical_exam_result',
        'resp_exam',
    )

    list_filter = (
        'general_activity',
        'abnormal_activity',
        'physical_exam_result',
    )

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

admin.site.register(InfantBirthExam, InfantBirthExamAdmin)
