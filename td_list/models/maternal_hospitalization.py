from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class MaternalHospitalization(ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Hospitalization"
        verbose_name_plural = "Maternal Hospitalizations"
