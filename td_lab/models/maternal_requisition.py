from django.db import models

# from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_export.models import ExportTrackingFieldsMixin
from edc_meta_data.managers import RequisitionMetaDataManager
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_visit_tracking.models.crf_model_mixin import CrfModelMixin, CrfModelManager
from lab_requisition.models import RequisitionModelMixin

from td_maternal.models import MaternalVisit

from .aliquot import Aliquot
from .aliquot_type import AliquotType
from .packing_list import PackingList
from .panel import Panel


class MaternalRequisitionManager(CrfModelManager):

    def get_by_natural_key(self, requisition_identifier):
        return self.get(requisition_identifier=requisition_identifier)


class MaternalRequisition(CrfModelMixin, SyncModelMixin, RequisitionModelMixin,
                          ExportTrackingFieldsMixin, BaseUuidModel):

    aliquot_model = Aliquot

    maternal_visit = models.ForeignKey(MaternalVisit)

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    aliquot_type = models.ForeignKey(AliquotType)

    panel = models.ForeignKey(Panel)

    objects = MaternalRequisitionManager()

    history = SyncHistoricalRecords()

    entry_meta_data_manager = RequisitionMetaDataManager(MaternalVisit)

    def __str__(self):
        return '{0} {1}'.format(str(self.panel), self.requisition_identifier)

    def natural_key(self):
        return (self.requisition_identifier,)

    class Meta:
        app_label = 'td_lab'
        verbose_name = 'Maternal Requisition'
        verbose_name_plural = 'Maternal Requisition'
        unique_together = ('maternal_visit', 'panel', 'is_drawn')
        ordering = ('-created', )
