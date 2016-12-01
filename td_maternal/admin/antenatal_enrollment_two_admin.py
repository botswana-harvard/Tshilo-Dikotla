from django.contrib import admin

from td.admin_mixins import ModelAdminMixin

from ..forms import AntenatalEnrollmentTwoForm
from ..models import AntenatalEnrollmentTwo
from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin


@admin.register(AntenatalEnrollmentTwo)
class AntenatalEnrollmentTwoAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    dashboard_type = 'maternal'
    form = AntenatalEnrollmentTwoForm

    radio_fields = {'antenatal_visits': admin.VERTICAL}

    list_display = ('subject_identifier', 'report_datetime', 'antenatal_visits')
