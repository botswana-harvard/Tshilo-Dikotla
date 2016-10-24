import factory

from django.utils import timezone

from edc_constants.constants import ALIVE

from td_infant.models import InfantVisit


class InfantVisitFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantVisit

    report_datetime = timezone.now()
    information_provider = 'Mother'
    study_status = 'onstudy rando ondrug'
    survival_status = ALIVE
    last_alive_date = timezone.now().date()
    reason = 'scheduled'
