from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class MaternalMedications (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Medications"
        verbose_name_plural = "Maternal Medications"
