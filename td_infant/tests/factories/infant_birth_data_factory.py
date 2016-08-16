import factory

from django.utils import timezone

from edc_constants.constants import YES

from td_infant.models import InfantBirthData


class InfantBirthDataFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantBirthData

    report_datetime = timezone.now()
    congenital_anomalities = YES
    weight_kg = '3'
    infant_length = '50'
    head_circumference = '10'
