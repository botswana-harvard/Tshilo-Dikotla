import factory
from datetime import timedelta

from django.utils import timezone

from edc_constants.constants import YES, NO

from .maternal_visit_factory import MaternalVisitFactory

from ...models import MaternalUltraSoundInitial


class MaternalUltraSoundIniFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalUltraSoundInitial

    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    report_datetime = timezone.now()
    number_of_gestations = 1
    bpd = 200
    hc = 200
    ac = 200
    fl = 200
    hl = 200
    ga_by_lmp = 100
    ga_by_ultrasound_wks = 7
    ga_by_ultrasound_days = 5
    est_fetal_weight = 700
    est_edd = timezone.now().date() + timedelta(days=90)
    edd_confirmed = timezone.now() + timedelta(days=90)
    ga_confirmed = 7
    amniotic_fluid_volume = 1
    lateral_ventricle = 100
    cerebellum = 100
    cistema_magna = 100
    malformations = 100

