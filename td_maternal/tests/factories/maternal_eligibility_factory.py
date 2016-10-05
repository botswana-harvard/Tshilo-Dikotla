import factory

from datetime import datetime

from edc_constants.constants import YES, NO

from td_maternal.models import MaternalEligibility


class MaternalEligibilityFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalEligibility

    report_datetime = datetime.today
    age_in_years = 26
