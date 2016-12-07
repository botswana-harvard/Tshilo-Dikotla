from django.contrib import admin

from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin

from td.admin_mixins import ModelAdminMixin

from ..admin_site import td_maternal_admin
from ..forms import AntenatalEnrollmentTwoForm
from ..models import AntenatalEnrollmentTwo


@admin.register(AntenatalEnrollmentTwo, site=td_maternal_admin)
class AntenatalEnrollmentTwoAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    dashboard_type = 'maternal'
    form = AntenatalEnrollmentTwoForm

    radio_fields = {'antenatal_visits': admin.VERTICAL}

    list_display = ('subject_identifier', 'report_datetime', 'antenatal_visits')
