import factory

from django.utils import timezone

from edc_constants.choices import YES, NO

from tshilo_dikotla.apps.td_maternal.models import AntenatalEnrollment


class AntenatalEnrollmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = AntenatalEnrollment

    report_datetime = timezone.now()

    gestation_wks = 36
    last_period_date = timezone.datetime.now()
    is_diabetic = NO
    valid_regimen = YES
    valid_regimen_duration = YES
    week32_test = YES
    will_breastfeed = YES
    will_remain_onstudy = YES
