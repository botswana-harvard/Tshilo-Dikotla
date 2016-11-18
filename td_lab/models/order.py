from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from edc_base.model.models import BaseUuidModel
from edc_export.model_mixins import ExportTrackingFieldsMixin
from edc_base.model.models import HistoricalRecords

from ..managers import OrderManager


class Order(ExportTrackingFieldsMixin, BaseUuidModel):

    order_datetime = models.DateTimeField(default=timezone.now)

    objects = OrderManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.order_datetime, )

    def items(self):
        change_list_url = reverse("admin:{}_{}_changelist".format(self._meta.app_label, 'orderitem'))
        return '<a href="{change_list_url}?q={pk}">{count} items</a>'.format(
            change_list_url=change_list_url, pk=self.id, count=self.order_items.count())
    items.allow_tags = True

#     @property
#     def order_items(self):
#         OrderItem = models.get_model('mb_lab', 'orderitem')
#         return OrderItem.objects.filter(order__pk=self.pk)

    class Meta:
        app_label = 'td_lab'
