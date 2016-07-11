from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class InfantVaccines (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Infant Vaccines"
        verbose_name_plural = "Infant Vaccines"
