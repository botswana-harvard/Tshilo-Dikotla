from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class DeliveryComplications(ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Delivery Complications"
        verbose_name_plural = "Delivery Complications"
