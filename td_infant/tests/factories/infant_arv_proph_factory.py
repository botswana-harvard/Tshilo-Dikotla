import factory

from django.utils import timezone

from edc_constants.constants import YES

from td_infant.models import InfantArvProph, InfantArvProphMod
from td_infant.choices import ARV_DRUG_LIST, ARV_MODIFICATION_REASON, DOSE_STATUS

from td.constants import NO_MODIFICATIONS


class InfantArvProphFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantArvProph

    prophylatic_nvp = YES
    arv_status = NO_MODIFICATIONS


class InfantArvProphModFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantArvProphMod

    infant_arv_proph = factory.SubFactory(InfantArvProphFactory)
    arv_code = ARV_DRUG_LIST[0][0]
    dose_status = DOSE_STATUS[0][0]
    modification_date = timezone.now().date()
    modification_code = ARV_MODIFICATION_REASON[0][0]
