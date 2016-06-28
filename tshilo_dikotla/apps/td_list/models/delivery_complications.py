from edc_base.model.models import BaseListModel


class DeliveryComplications(BaseListModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Delivery Complications"
        verbose_name_plural = "Delivery Complications"
