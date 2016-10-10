import factory
from django.utils import timezone

from .appointment_factory import AppointmentFactory

from td_maternal.models import MaternalVisit


class MaternalVisitFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalVisit

    report_datetime = timezone.now()
    appointment = factory.SubFactory(AppointmentFactory)
    info_source = "participant"
