from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..forms import MaternalUltraSoundInitialForm
from ..models import MaternalUltraSoundInitial
from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalUltraSoundInitialAdmin(BaseMaternalModelAdmin):

    form = MaternalUltraSoundInitialForm

    fields = ('maternal_visit',
              'report_datetime',
              'number_of_gestations',
              'bpd',
              'hc',
              'ac',
              'fl',
              'hl',
              'ga_by_lmp',
              'ga_by_ultrasound_wks',
              'ga_by_ultrasound_days',
              'ga_confirmed',
              'est_fetal_weight',
              'est_edd',
              'edd_confirmed',
              'lateral_ventricle',
              'cerebellum',
              'cistema_magna',
              'malformations')

    readonly_fields = ('edd_confirmed', 'ga_confirmed', 'ga_by_lmp')

    radio_fields = {'number_of_gestations': admin.VERTICAL,
                    'malformations': admin.VERTICAL}

    list_display = ('report_datetime', 'number_of_gestations', 'ga_confrimation_method', 'edd_confirmed',
                    'ga_confirmed', 'ga_by_lmp')

    list_filter = ('report_datetime', 'number_of_gestations', 'malformations', 'ga_confrimation_method')

admin.site.register(MaternalUltraSoundInitial, MaternalUltraSoundInitialAdmin)
