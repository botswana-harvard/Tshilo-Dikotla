import factory

from datetime import datetime

from .registered_subject_factory import RegisteredSubjectFactory
from edc_constants.choices import YES

from td_maternal.models import AntenatalEnrollmentTwo


class AntenatalEnrollmentTwoFactory(factory.DjangoModelFactory):

    class Meta:
        model = AntenatalEnrollmentTwo

    report_datetime = datetime.now()
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    antenatal_visits = YES


