import factory

from django.utils import timezone

from td_infant.models import InfantBirth
from td_maternal.tests.factories import MaternalLabourDelFactory


class InfantBirthFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantBirth

    report_datetime = timezone.now()
    maternal_labour_del = factory.SubFactory(MaternalLabourDelFactory)
    first_name = 'BABY'
    initials = 'BB'
    dob = timezone.now().date()
    gender = 'F'
