from django import forms
from td_appointment.models import Appointment


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = '__all__'
