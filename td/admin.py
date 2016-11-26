from django.contrib import admin

from edc_registration.admin import RegisteredSubjectModelAdminMixin

from tshilo_dikotla.admin_mixins import ModelAdminMixin

from .forms import AppointmentForm
from .models import Appointment, RegisteredSubject


@admin.register(RegisteredSubject)
class RegisteredSubjectAdmin(RegisteredSubjectModelAdminMixin, admin.ModelAdmin):
    pass


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
