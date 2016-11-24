from django.contrib import admin

from edc_export.actions import export_as_csv_action

from tshilo_dikotla.admin_mixins import ModelAdminMixin

from ..forms import MaternalInterimIdccForm
from ..models import MaternalInterimIdcc
from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(MaternalInterimIdcc)
class MaternalInterimIdccAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalInterimIdccForm

    radio_fields = {'info_since_lastvisit': admin.VERTICAL,
                    'value_vl_size': admin.VERTICAL}

    list_display = ('report_datetime', 'recent_cd4', 'value_vl',)

    list_filter = ('info_since_lastvisit', 'recent_cd4_date', 'value_vl_size', 'recent_vl_date')
