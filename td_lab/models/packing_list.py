from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_export.models import ExportTrackingFieldsMixin
from edc_lab.lab_packing.models import PackingListMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords

from ..managers import PackingListManager


class PackingList(PackingListMixin, SyncModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    objects = PackingListManager()

    history = SyncHistoricalRecords()

#     @property
#     def item_models(self):
#         item_m = []
#         item_m.append(models.get_model('mb_lab', 'InfantRequisition'))
#         item_m.append(models.get_model('mb_lab', 'MaternalRequisition'))
#         item_m.append(models.get_model('mb_lab', 'Aliquot'))
#         return item_m
# 
#     @property
#     def packing_list_item_model(self):
#         return models.get_model('mb_lab', 'PackingListItem')

    class Meta:
        app_label = 'td_lab'
        verbose_name = 'Packing List'
