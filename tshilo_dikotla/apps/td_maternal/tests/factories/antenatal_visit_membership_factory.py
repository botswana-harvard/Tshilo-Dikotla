import factory

from datetime import datetime
from django.utils import timezone

from edc_registration.tests.factories import RegisteredSubjectFactory
from edc_constants.choices import YES, NO, POS, NEG, NOT_APPLICABLE

from tshilo_dikotla.apps.td_maternal.models import AntenatalVisitMembership


class AntenatalVisitMembershipFactory(factory.DjangoModelFactory):

    class Meta:
        model = AntenatalVisitMembership

    report_datetime = timezone.now()
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    antenatal_visits = YES


