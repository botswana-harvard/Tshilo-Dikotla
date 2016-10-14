from django.contrib import admin

from edc_base.modeladmin.mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
    ModelAdminAuditFieldsMixin)
from td_appointment.models import Appointment
from td_appointment.forms import AppointmentForm


class MembershipBaseModelAdmin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                               ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin, admin.ModelAdmin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

    def redirect_url(self, request, obj, post_url_continue=None):
        return request.GET.get('next')


class AppointmentAdmin(MembershipBaseModelAdmin):

    fields = (
        'appt_datetime',
        'appt_type',
        'appt_status',
        'appt_reason',
        'comment',
    )

    radio_fields = {
        'appt_type': admin.VERTICAL,
        'appt_status': admin.VERTICAL}

    form = AppointmentForm

admin.site.register(Appointment, AppointmentAdmin)

