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
                        UpdatesRequisitionMetadataModelMixin, UrlMixin, BaseUuidModel):

    aliquot_model = Aliquot

    infant_visit = models.ForeignKey(InfantVisit)

#     packing_list = models.ForeignKey(PackingList, null=True, blank=True)

#     aliquot_type = models.ForeignKey(AliquotType)

    panel = models.ForeignKey(Panel)

#     objects = InfantRequisitionManager()

    history = SyncHistoricalRecords()

#     entry_meta_data_manager = RequisitionMetaDataManager(InfantVisit)

    @property
    def subject_identifier(self):
        return self.infant_visit.appointment.subject_identifier

    def aliquot(self):
        return """<a href="#" />aliquot</a>"""
    aliquot.allow_tags = True

    @property
    def visit(self):
        return getattr(self, 'infant_visit')

    def get_visit(self):
        return self.infant_visit

    def save(self, *args, **kwargs):
        if not self.id:
            try:
                self.panel = Panel.objects.get(name=self.panel_name)
            except Panel.DoesNotExist:
                self.panel = Panel.objects.create(name=self.panel_name)
        super(InfantRequisition, self).save(*args, **kwargs)

    class Meta:
        app_label = 'td_lab'
        verbose_name = 'Infant Laboratory Requisition'
        verbose_name_plural = 'Infant Laboratory Requisition'
        unique_together = ('infant_visit', 'panel_name', 'is_drawn')
