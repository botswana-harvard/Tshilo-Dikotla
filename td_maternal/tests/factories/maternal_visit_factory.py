from edc_constants.constants import SCHEDULED

from django.utils import timezone
import factory

from edc_appointment.tests.factories import AppointmentFactory
from td_maternal.models import MaternalVisit


class MaternalVisitFactory(factory.DjangoModelFactory):

    report_datetime = timezone.now()
    appointment = factory.SubFactory(AppointmentFactory)
    reason = SCHEDULED
    info_source = "participant"

    class Meta:
        model = MaternalVisit
