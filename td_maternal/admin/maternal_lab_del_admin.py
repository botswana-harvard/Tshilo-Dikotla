from django.contrib import admin

from td.admin_mixins import ModelAdminMixin

from ..forms import MaternalLabDelForm, MaternalHivInterimHxForm
from ..models import MaternalLabDel, MaternalHivInterimHx

from .base_maternal_model_admin import BaseMaternalModelAdmin
from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin


@admin.register(MaternalLabDel)
class MaternalLabDelAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    dashboard_type = 'maternal'
    form = MaternalLabDelForm

    list_display = ('subject_identifier',
                    'delivery_datetime',
                    'labour_hrs',
                    'delivery_hospital',
                    'valid_regiment_duration')

    list_filter = ('delivery_hospital',
                   'valid_regiment_duration')

    search_fields = ('subject_identifier', )
    readonly_fields = ('live_infants_to_register',)

    radio_fields = {'delivery_time_estimated': admin.VERTICAL,
                    'delivery_hospital': admin.VERTICAL,
                    'valid_regiment_duration': admin.VERTICAL,
                    'mode_delivery': admin.VERTICAL,
                    'csection_reason': admin.VERTICAL,
                    'csection_reason': admin.VERTICAL, }
    filter_horizontal = ('delivery_complications',)


@admin.register(MaternalHivInterimHx)
class MaternalHivInterimHxAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalHivInterimHxForm

    radio_fields = {'has_cd4': admin.VERTICAL,
                    'has_vl': admin.VERTICAL,
                    'vl_detectable': admin.VERTICAL}
