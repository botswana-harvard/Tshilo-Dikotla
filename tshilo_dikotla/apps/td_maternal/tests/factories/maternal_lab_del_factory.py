import factory

from datetime import datetime
from django.utils import timezone

from edc_registration.tests.factories import RegisteredSubjectFactory
from edc_constants.choices import YES, NO, POS, NEG, NOT_APPLICABLE

from tshilo_dikotla.apps.td_maternal.models import MaternalLabourDel


class MaternalLabourDelFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalLabourDel

    report_datetime = timezone.now()
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    delivery_datetime = timezone.now()
    delivery_time_estimated = NO
    labour_hrs = '3'
    delivery_hospital = 'Lesirane'
    has_uterine_tender = NO
    has_temp = NO
    has_chorioamnionitis = NO
    delivery_complications = NO
    live_infants_to_register = 1

