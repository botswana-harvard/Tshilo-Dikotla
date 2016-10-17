from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..forms import MaternalAztNvpForm
from ..models import MaternalAztNvp
from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(MaternalAztNvp)
class MaternalAztNvpAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalAztNvpForm

    radio_fields = {'azt_nvp_delivery': admin.VERTICAL,
                    'instructions_given': admin.VERTICAL}

    list_display = ('report_datetime', 'date_given', 'azt_nvp_delivery', 'instructions_given')

    list_filter = ('report_datetime', 'date_given', 'azt_nvp_delivery', 'instructions_given')
