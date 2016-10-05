import factory

from django.utils import timezone

from .registered_subject_factory import RegisteredSubjectFactory
from edc_constants.choices import YES, NO, POS, NEG, NOT_APPLICABLE

from td_maternal.models import MaternalRando

from .maternal_visit_factory import MaternalVisitFactory


class MaternalRandomizationFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalRando

    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    report_datetime = timezone.now()
    site = 'Gsaborone'
    sid = 1
    rx = 'NVP'
    subject_identifier = '085-0000000-1'
    randomization_datetime = timezone.now()
    initials = 'IN'


