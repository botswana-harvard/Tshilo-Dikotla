import factory

from datetime import datetime
from django.utils import timezone

from edc_registration.tests.factories import RegisteredSubjectFactory
from edc_constants.choices import YES, NO, POS, NEG, NOT_APPLICABLE

from tshilo_dikotla.apps.td_maternal.models import AntenatalEnrollment


class AntenatalEnrollmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = AntenatalEnrollment

    report_datetime = timezone.now()

    gestation_wks_lmp = 34
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    last_period_date = timezone.datetime.date(datetime.today())
    is_diabetic = NO
    week32_test = NO
    will_breastfeed = YES
    current_hiv_status = NEG
    will_remain_onstudy = YES
    evidence_hiv_status = NO
    rapid_test_done = YES
    rapid_test_result = NEG
    rapid_test_date = timezone.datetime.now()
    valid_regimen = NOT_APPLICABLE
    valid_regimen_duration = NOT_APPLICABLE
