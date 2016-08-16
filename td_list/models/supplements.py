from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class Supplements (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Supplements"
        verbose_name_plural = "Supplements"
