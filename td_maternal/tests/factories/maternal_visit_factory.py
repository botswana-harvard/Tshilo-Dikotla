import factory
from django.utils import timezone

from edc_appointment.tests.factories import AppointmentFactory
from edc_constants.constants import SCHEDULED

from td_maternal.models import MaternalVisit


class MaternalVisitFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalVisit

    report_datetime = timezone.now()
    appointment = factory.SubFactory(AppointmentFactory)
    reason = SCHEDULED
    info_source = "participant"
