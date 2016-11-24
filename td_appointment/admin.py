from django.contrib import admin

from td_appointment.models import Appointment
from td_appointment.forms import AppointmentForm

from tshilo_dikotla.admin_mixins import ModelAdminMixin


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
