import factory

from django.utils import timezone

from .registered_subject_factory import RegisteredSubjectFactory
from edc_constants.choices import YES, NO, NOT_APPLICABLE

from td_maternal.models import MaternalLabourDel


class MaternalLabourDelFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalLabourDel

    report_datetime = timezone.now()
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    delivery_datetime = timezone.now()
    delivery_time_estimated = NO
    labour_hrs = '3'
    delivery_hospital = 'Lesirane'
    mode_delivery = 'spontaneous vaginal'
    csection_reason = NOT_APPLICABLE
    live_infants_to_register = 1
    valid_regiment_duration = YES

