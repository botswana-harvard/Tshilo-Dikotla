from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..forms import MaternalUltraSoundFuForm
from ..models import MaternalUltraSoundFu
from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalUltraSoundFuAdmin(BaseMaternalModelAdmin):

    form = MaternalUltraSoundFuForm

    fields = ('maternal_visit',
              'report_datetime',
              'bpd',
              'hc',
              'ac',
              'fl',
#               'hl',
#               'lateral_ventricle',
#               'cerebellum',
#               'cistema_magna'
    )

    list_display = ('maternal_visit', 'report_datetime')

    list_filter = ('report_datetime', )

#     filter_horizontal = ('malformations',)

admin.site.register(MaternalUltraSoundFu, MaternalUltraSoundFuAdmin)
