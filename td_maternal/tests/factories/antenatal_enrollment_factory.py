import factory

from django.utils import timezone

from edc_constants.constants import YES, NO, NEG, NOT_APPLICABLE

from td_maternal.models import AntenatalEnrollment


class AntenatalEnrollmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = AntenatalEnrollment

    report_datetime = timezone.now()
    subject_identifier = None
    knows_lmp = YES,
    last_period_date = timezone.now().date()
    is_diabetic = NO
    week32_test = NO
    will_breastfeed = YES
    current_hiv_status = NEG
    will_remain_onstudy = YES
    evidence_hiv_status = NO
    evidence_32wk_hiv_status = NOT_APPLICABLE
    rapid_test_done = YES
    rapid_test_result = NEG
    rapid_test_date = timezone.now().date()
    will_get_arvs = NOT_APPLICABLE
