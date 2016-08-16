import factory

from django.utils import timezone

from edc_constants.constants import NO, YES
from edc_constants.choices import DRUG_ROUTE

from td_maternal.models import MaternalObstericalHistory

from .maternal_visit_factory import MaternalVisitFactory


class MaternalObstericHistoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalObstericalHistory

    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    report_datetime = timezone.now()
    prev_pregnancies = 1
    pregs_24wks_or_more = 1
    lost_before_24wks = 0
    lost_after_24wks = 0
    live_children = 0
    children_died_b4_5yrs = 0
    children_deliv_before_37wks = 0
    children_deliv_aftr_37wks = 1