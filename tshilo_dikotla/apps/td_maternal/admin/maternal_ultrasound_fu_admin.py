from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
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
              'hl',
              'amniotic_fluid_volume',
              'lateral_ventricle',
              'cerebellum',
              'cistema_magna',
              'malformations')

    radio_fields = {'amniotic_fluid_volume': admin.VERTICAL,
                    'malformations': admin.VERTICAL}

    list_display = ('maternal_visit', 'report_datetime', 'lateral_ventricle', 'cerebellum')

    list_filter = ('report_datetime', )

admin.site.register(MaternalUltraSoundFu, MaternalUltraSoundFuAdmin)
