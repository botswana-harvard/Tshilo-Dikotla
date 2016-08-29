import factory

from django.utils import timezone

from edc_constants.choices import YES

from td_maternal.models import MaternalInterimIdcc

from .maternal_visit_factory import MaternalVisitFactory


class MaternalInterimIdccFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalInterimIdcc

    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    report_datetime = timezone.now()
    info_since_lastvisit = YES
    recent_cd4 = 40
    recent_cd4_date = timezone.now()