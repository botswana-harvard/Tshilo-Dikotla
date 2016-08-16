from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class MaternalRelatives(ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Relatives"
        verbose_name_plural = "Maternal Relatives"
