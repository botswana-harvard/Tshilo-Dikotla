import factory

from django.utils import timezone

from td_appointment.models import Appointment
from .registered_subject_factory import RegisteredSubjectFactory


class AppointmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = Appointment

    # registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    appt_datetime = timezone.now()
    best_appt_datetime = timezone.now()
    appt_close_datetime = timezone.now()
    # study_site = '40'
    visit_instance = '0'
