from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class MaternalDiagnoses(ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Diagnoses"
        verbose_name_plural = "Maternal Diagnoses"