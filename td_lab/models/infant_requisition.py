from django.db import models

from edc_base.model.models import BaseUuidModel, UrlMixin
from edc_export.models import ExportTrackingFieldsMixin
# from edc_meta_data.managers import RequisitionMetaDataManager
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_visit_tracking.model_mixins import CrfModelMixin
from edc_lab.requisition.model_mixins import RequisitionModelMixin
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import UpdatesRequisitionMetadataModelMixin

from td_infant.models import InfantVisit

from .aliquot import Aliquot
from td_lab.models.panel import Panel
# from .aliquot_type import AliquotType
# from .packing_list import PackingList
# from .panel import Panel


# class InfantRequisitionManager(CrfModelManager):
#
#     def get_by_natural_key(self, requisition_identifier):
#         return self.get(requisition_identifier=requisition_identifier)


class InfantRequisition(CrfModelMixin, SyncModelMixin, RequisitionModelMixin, ExportTrackingFieldsMixin,
                        RequiresConsentMixin, UpdatesRequisitionMetadataModelMixin, UrlMixin, BaseUuidModel):

    aliquot_model = Aliquot

    infant_visit = models.ForeignKey(InfantVisit)

#     packing_list = models.ForeignKey(PackingList, null=True, blank=True)

#     aliquot_type = models.ForeignKey(AliquotType)

    panel = models.ForeignKey(Panel)

#     objects = InfantRequisitionManager()

    history = SyncHistoricalRecords()

#     entry_meta_data_manager = RequisitionMetaDataManager(InfantVisit)

    def get_visit(self):
        return self.infant_visit

    class Meta:
        app_label = 'td_lab'
        consent_model = 'td_maternal.maternalconsent'
        verbose_name = 'Infant Laboratory Requisition'
        verbose_name_plural = 'Infant Laboratory Requisition'
        unique_together = ('infant_visit', 'panel_name', 'is_drawn')
