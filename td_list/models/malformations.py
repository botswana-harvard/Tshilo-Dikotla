from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class Malformations(ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Fetal Malformations"
        verbose_name_plural = "Fetal Malformations"
