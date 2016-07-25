import factory

from edc_constants.constants import YES

from td_infant.models import InfantFuDx, InfantFuDxItems
# from microbiome.apps.mb.choices import DX_INFANT

from .infant_visit_factory import InfantVisitFactory


class InfantFuDxFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantFuDx

    infant_visit = factory.SubFactory(InfantVisitFactory)

# class InfantFuDxItemsFactory(factory.DjangoModelFactory):
# 
#     class Meta:
#         model = InfantFuDxItems
# 
#     infant_fu_dx = factory.SubFactory(InfantFuDx)
#     fu_dx = DX_INFANT[0][0]
#     health_facility = YES
#     was_hospitalized = YES
