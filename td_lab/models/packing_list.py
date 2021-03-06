from django.apps import apps
from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_export.models import ExportTrackingFieldsMixin
from edc_lab.lab_packing.models import PackingListMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords

from ..managers import PackingListManager


class PackingList(PackingListMixin, SyncModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    objects = PackingListManager()

    history = SyncHistoricalRecords()

    @property
    def item_models(self):
        item_m = []
        item_m.append(apps.get_model('td_lab', 'InfantRequisition'))
        item_m.append(apps.get_model('td_lab', 'MaternalRequisition'))
        item_m.append(apps.get_model('td_lab', 'Aliquot'))
        return item_m

    @property
    def packing_list_item_model(self):
        return apps.get_model('td_lab', 'PackingListItem')

    def specimen_count(self):
        lst = self.list_items.replace('\r', '').split('\n')
        return len(lst)

    def view_list_items(self):
        return '<a href="/admin/{app_label}/{object_name}item/?q={reference}">{count} items</a>'.format(
            app_label=self._meta.app_label,
            object_name=self._meta.object_name.lower(),
            reference=self.timestamp,
            count=self.specimen_count())
    view_list_items.allow_tags = True

    class Meta:
        app_label = 'td_lab'
        verbose_name = 'Packing List'
