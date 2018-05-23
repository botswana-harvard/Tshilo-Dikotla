from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_base.model.fields import OtherCharField
from edc_export.models import ExportTrackingFieldsMixin
from edc_meta_data.managers import RequisitionMetaDataManager
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_visit_tracking.models import CrfModelManager, CrfModelMixin
from lab_requisition.models import RequisitionModelMixin

from td_infant.models import InfantVisit

from .aliquot import Aliquot
from .aliquot_type import AliquotType
from .packing_list import PackingList
from .panel import Panel
from .receive import Receive


class InfantRequisitionManager(CrfModelManager):

    def get_by_natural_key(self, requisition_identifier):
        return self.get(requisition_identifier=requisition_identifier)


class InfantRequisition(CrfModelMixin, SyncModelMixin, RequisitionModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    aliquot_model = Aliquot

    infant_visit = models.ForeignKey(InfantVisit)

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    aliquot_type = models.ForeignKey(AliquotType)

    panel = models.ForeignKey(Panel)

    reason_not_drawn_other = OtherCharField(
        max_length=35,
        verbose_name="if (other) specify...",
        blank=True,
        null=True)

    objects = InfantRequisitionManager()

    history = SyncHistoricalRecords()

    entry_meta_data_manager = RequisitionMetaDataManager(InfantVisit)

    def save(self, *args, **kwargs):
        if self.id:
            try:
                receive = Receive.objects.get(requisition_identifier=self.requisition_identifier)
            except Receive.DoesNotExist:
                pass
            else:
                receive.drawn_datetime = self.drawn_datetime
                receive.save()
        super(RequisitionModelMixin, self).save(*args, **kwargs)

    def get_visit(self):
        return self.infant_visit

    class Meta:
        app_label = 'td_lab'
        verbose_name = 'Infant Laboratory Requisition'
        verbose_name_plural = 'Infant Laboratory Requisition'
        unique_together = ('infant_visit', 'panel', 'is_drawn')
