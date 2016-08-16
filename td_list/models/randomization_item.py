from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class RandomizationItem (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Randomization Item"
        verbose_name_plural = "Maternal Randomization Item"
