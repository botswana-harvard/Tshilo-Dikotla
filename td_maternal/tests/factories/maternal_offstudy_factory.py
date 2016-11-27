import factory

from django.utils import timezone

from td_maternal.models import MaternalOffstudy

from .maternal_visit_factory import MaternalVisitFactory


class MaternalOffstudyFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalOffstudy

    offstudy_date = timezone.now().date()

    maternal_visit = factory.SubFactory(MaternalVisitFactory)
