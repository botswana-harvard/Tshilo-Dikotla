import factory

from django.utils import timezone
from td_infant.models import InfantFuImmunizations
from .infant_visit_factory import InfantVisitFactory
from edc_constants.constants import YES


class InfantFuImmunizationsFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantFuImmunizations

    report_datetime = timezone.now()
    vaccines_received = YES
    vaccines_missed = YES

