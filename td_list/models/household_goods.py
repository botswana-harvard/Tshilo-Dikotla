from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class HouseholdGoods (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Household Goods"
        verbose_name_plural = "Household Goods"
