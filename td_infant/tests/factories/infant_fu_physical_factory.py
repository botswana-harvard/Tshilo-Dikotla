import factory

from django.utils import timezone

from edc_constants.constants import YES

from td_infant.models import InfantFuPhysical

from .infant_visit_factory import InfantVisitFactory


class InfantFuPhysicalFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantFuPhysical

    infant_visit = factory.SubFactory(InfantVisitFactory)
    report_datetime = timezone.now()
    weight_kg = 3
    height = 45
    head_circumference = 18
    general_activity = "NORMAL"
    physical_exam_result = "NORMAL"
    heent_exam = YES
