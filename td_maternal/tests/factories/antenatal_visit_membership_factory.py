import factory

from datetime import datetime
from django.utils import timezone

from .registered_subject_factory import RegisteredSubjectFactory
from edc_constants.choices import YES, NO, POS, NEG, NOT_APPLICABLE

from td_maternal.models import AntenatalVisitMembership


class AntenatalVisitMembershipFactory(factory.DjangoModelFactory):

    class Meta:
        model = AntenatalVisitMembership

    report_datetime = timezone.now()
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    antenatal_visits = YES


