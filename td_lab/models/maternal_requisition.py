from django.db import models

from django.apps import apps as django_apps
from edc_base.model.models import BaseUuidModel, UrlMixin
from edc_export.models import ExportTrackingFieldsMixin
# from edc_meta_data.managers import RequisitionMetaDataManager
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_visit_tracking.model_mixins import CrfModelMixin # , CrfModelManager
from edc_lab.requisition.model_mixins import RequisitionModelMixin
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import UpdatesRequisitionMetadataModelMixin

from td_maternal.models import MaternalVisit

from .aliquot import Aliquot
from td_lab.models.panel import Panel
# from .aliquot_type import AliquotType
# from .packing_list import PackingList
# from .panel import Panel


# class MaternalRequisitionManager(CrfModelManager):
#
#     def get_by_natural_key(self, requisition_identifier):
#         return self.get(requisition_identifier=requisition_identifier)


class MaternalRequisition(CrfModelMixin, SyncModelMixin, RequisitionModelMixin, ExportTrackingFieldsMixin,
                          RequiresConsentMixin, UpdatesRequisitionMetadataModelMixin, UrlMixin, BaseUuidModel):

    aliquot_model = Aliquot

    maternal_visit = models.ForeignKey(MaternalVisit)

#     packing_list = models.ForeignKey(PackingList, null=True, blank=True)
#
#     aliquot_type = models.ForeignKey(AliquotType)
#
    panel = models.ForeignKey(Panel)

#     objects = MaternalRequisitionManager()

    @property
    def subject_identifier(self):
        return self.maternal_visit.appointment.subject_identifier

    history = SyncHistoricalRecords()

#     entry_meta_data_manager = RequisitionMetaDataManager(MaternalVisit)

#     @classmethod
#     def visit_model_attr(cls):
#         app_config = django_apps.get_app_config('edc_visit_tracking')
#         print(cls._meta.label_lower, "cls._meta.label_lower, cls._meta.label_lower")
#         return app_config.visit_model_attr(cls._meta.label_lower)

    @property
    def visit(self):
        return getattr(self, 'maternal_visit')

    @property
    def metadata_query_options(self):
        options = self.maternal_visit.metadata_query_options
        options.update({
            'subject_identifier': self.maternal_visit.appointment.subject_identifier,
            'model': 'td_lab.maternalrequisition',
            'visit_code': self.maternal_visit.visit_code,
            'panel_name': self.panel_name,
        })
        return options

    def __str__(self):
        return '{0} {1}'.format(str(self.panel_name), self.requisition_identifier)

    def natural_key(self):
        return (self.requisition_identifier,)

    def save(self, *args, **kwargs):
        if not self.id:
            self.panel = Panel.objects.create(name=self.panel_name)
        super(MaternalRequisition, self).save(*args, **kwargs)

    class Meta:
        app_label = 'td_lab'
        consent_model = 'td_maternal.maternalconsent'
        verbose_name = 'Maternal Requisition'
        verbose_name_plural = 'Maternal Requisition'
        unique_together = ('maternal_visit', 'panel_name', 'is_drawn')
        ordering = ('-created', )
