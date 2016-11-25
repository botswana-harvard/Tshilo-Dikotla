import factory

from django.utils import timezone

from edc_constants.constants import YES

from td_maternal.models import MaternalEligibility


class MaternalEligibilityFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalEligibility

    report_datetime = timezone.now()
    age_in_years = 26
    has_omang = YES
