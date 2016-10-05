from django.apps import apps as django_apps
from django.core.urlresolvers import reverse
from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_export.models import ExportTrackingFieldsMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_lab.aliquot.model_mixins import AliquotModelMixin
from edc_lab.aliquot.managers import AliquotManager

# from .aliquot_condition import AliquotCondition
# from .aliquot_type import AliquotType
# from .receive import Receive


class Aliquot(SyncModelMixin, AliquotModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):

#     receive = models.ForeignKey(
#         Receive,
#         editable=False)
# 
#     aliquot_type = models.ForeignKey(
#         AliquotType,
#         verbose_name="Aliquot Type",
#         null=True)
# 
#     aliquot_condition = models.ForeignKey(
#         AliquotCondition,
#         verbose_name="Aliquot Condition",
#         null=True,
#         blank=True)

    objects = AliquotManager()

    history = SyncHistoricalRecords()

    def save(self, *args, **kwargs):
        self.subject_identifier = self.receive.registered_subject.subject_identifier
        super(Aliquot, self).save(*args, **kwargs)

    @property
    def specimen_identifier(self):
        return self.aliquot_identifier[:-4]

    @property
    def aliquot_count(self):
        return int(self.aliquot_identifier[-2:])

    @property
    def registered_subject(self):
        return self.receive.registered_subject

    @property
    def requisition(self):
        model_name = self.receive.requisition_model_name
        model = django_apps.get_model(self._meta.app_label, model_name)
        return model.objects.get(requisition_identifier=self.receive.requisition_identifier)

    @property
    def visit_code(self):
        return self.receive.visit

    def processing(self):
        url = reverse('admin:td_lab_aliquotprocessing_add')
        return '<a href="{0}?aliquot={1}">process</a>'.format(url, self.pk)
    processing.allow_tags = True

    def label_context(self, ):
        label_context = {}
        primary = ''
        if self.aliquot_identifier[-2:] == '01':
            primary = '<'
        label_context.update({
            'aliquot_count': self.aliquot_count,
            'aliquot_identifier': self.aliquot_identifier,
            'aliquot_type': self.aliquot_type.name,
            'clinician_initials': self.requisition.clinician_initials,
            'drawn_datetime': self.requisition.drawn_datetime,
            'primary': primary,
            'site': self.requisition.study_site,
        })
        return label_context

    class Meta(AliquotModelMixin.Meta):
        app_label = 'td_lab'
        unique_together = (('parent_identifier', 'count'), )
