from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class ChronicConditions(ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Chronic Conditions"
        verbose_name_plural = "Chronic Conditions"
