from django.contrib import admin

from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin

from td.admin_mixins import ModelAdminMixin

from ..admin_site import td_maternal_admin
from ..forms import MaternalLabDelForm
from ..models import MaternalLabDel


@admin.register(MaternalLabDel, site=td_maternal_admin)
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
