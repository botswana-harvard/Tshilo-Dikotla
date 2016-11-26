from django.contrib import admin

from td.admin_mixins import ModelAdminMixin

from .forms import AppointmentForm
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(ModelAdminMixin):

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
