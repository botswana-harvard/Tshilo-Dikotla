import factory

from django.utils import timezone

from edc_constants.constants import NO, YES

from td_infant.models import InfantBirthArv

from .infant_visit_factory import InfantVisitFactory


class InfantBirthArvFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantBirthArv

    infant_visit = factory.SubFactory(InfantVisitFactory)
    azt_after_birth = NO
    azt_dose_date = timezone.now().date()
    azt_additional_dose = NO
    sdnvp_after_birth = NO
    nvp_dose_date = None
    azt_discharge_supply = NO
    infant_arv_comments = None
