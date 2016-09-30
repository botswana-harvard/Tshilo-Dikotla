from django.contrib import admin

from ..models import RapidTestResult

from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(RapidTestResult)
class RapidTestResultAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):
    fields = ('maternal_visit',
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
