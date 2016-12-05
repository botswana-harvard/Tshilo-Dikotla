import factory

from django.utils import timezone

from td_maternal.tests.factories import RegisteredSubjectFactory

from td_infant.models import InfantBirth
from td_maternal.tests.factories import MaternalLabDelFactory


class InfantBirthFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantBirth

    report_datetime = timezone.now()
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    maternal_labour_del = factory.SubFactory(MaternalLabDelFactory)
    first_name = 'BABY'
    initials = 'BB'
    dob = timezone.now().date()
    gender = 'F'
