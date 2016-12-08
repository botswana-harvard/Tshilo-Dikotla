from django.contrib import admin

from ..admin_site import td_maternal_admin
from ..models import RapidTestResult

from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(RapidTestResult, site=td_maternal_admin)
class RapidTestResultAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):
    fields = ('maternal_visit',
              'report_datetime',
              'rapid_test_done',
              'result_date',
              'result',
              'comments')
    list_display = ('maternal_visit',
                    'rapid_test_done',
                    'result')
    list_filter = ('rapid_test_done', 'result')
    search_fields = ('result_date', )
    radio_fields = {"rapid_test_done": admin.VERTICAL,
                    "result": admin.VERTICAL, }
