import factory

from django.utils import timezone

from edc_constants.constants import YES, NO

from td_infant.models import InfantNvpDispensing


class InfantNvpDispensingFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantNvpDispensing

    nvp_prophylaxis = YES
    azt_prophylaxis = NO
    nvp_admin_date = timezone.now().date()
    medication_instructions = YES
    dose_admin_infant = '10'
    correct_dose = YES
