import factory

from django.utils import timezone

from edc_registration.tests.factories import RegisteredSubjectFactory
from edc_constants.choices import YES, NO, POS, NEG, NOT_APPLICABLE

from td_maternal.models import RapidTestResult

from .maternal_visit_factory import MaternalVisitFactory


class RapidTestResultFactory(factory.DjangoModelFactory):

    class Meta:
        model = RapidTestResult

    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    report_datetime = timezone.now()
    rapid_test_done = YES
    result_date = timezone.datetime.today()
    result = POS



