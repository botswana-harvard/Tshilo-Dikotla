from django.contrib import admin

from ..models import MaternalOffStudy
from ..forms import MaternalOffStudyForm
from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalOffStudyAdmin(BaseMaternalModelAdmin):

    form = MaternalOffStudyForm

    fields = (
        'maternal_visit',
        'report_datetime',
        'offstudy_date',
        'reason',
        'reason_other',
        'comment')

admin.site.register(MaternalOffStudy, MaternalOffStudyAdmin)
