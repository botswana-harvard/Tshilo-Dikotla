from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class Rations (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Rations"
        verbose_name_plural = "Rations"
