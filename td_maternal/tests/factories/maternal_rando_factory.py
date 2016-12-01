import factory

from django.utils import timezone

from td_maternal.models import MaternalRando

from .maternal_visit_factory import MaternalVisitFactory


class MaternalRandoFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalRando

    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    report_datetime = timezone.now()
    site = 'Gaborone'
    sid = 1
    rx = 'NVP'
    subject_identifier = '085-0000000-1'
    randomization_datetime = timezone.now()
    initials = 'IN'
