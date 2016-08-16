from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class Foods (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Foods"
        verbose_name_plural = "Foods"
