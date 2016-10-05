import factory

from datetime import datetime
from django.utils import timezone

from .registered_subject_factory import RegisteredSubjectFactory
from edc_constants.choices import YES, NO, POS, NEG, NOT_APPLICABLE

from td_maternal.models import MaternalArvPreg
from tshilo_dikotla.constants import LIVE, STILL_BIRTH

from ..factories import MaternalVisitFactory


class MaternalArvPregFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalArvPreg

    report_datetime = timezone.datetime.now()
    took_arv = YES
    is_interrupt = NO
    interrupt = NOT_APPLICABLE
