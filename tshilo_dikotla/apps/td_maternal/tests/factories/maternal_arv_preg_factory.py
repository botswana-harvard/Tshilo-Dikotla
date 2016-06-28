import factory

from datetime import datetime
from django.utils import timezone

from edc_registration.tests.factories import RegisteredSubjectFactory
from edc_constants.choices import YES, NO, POS, NEG, NOT_APPLICABLE

from tshilo_dikotla.apps.td_maternal.models import MaternalArvPreg
from tshilo_dikotla.apps.td.constants import LIVE, STILL_BIRTH

from ..factories import MaternalVisitFactory


class MaternalArvPregFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalArvPreg

    report_datetime = timezone.datetime.now()
    took_arv = YES
    is_interrupt = NO
    interrupt = NOT_APPLICABLE
    