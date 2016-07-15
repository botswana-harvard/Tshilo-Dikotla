from django.core.urlresolvers import reverse
from django.db import models

# from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_export.models import ExportTrackingFieldsMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from lis.specimen.lab_aliquot.managers import AliquotManager
from lis.specimen.lab_aliquot.models import BaseAliquot

from .aliquot_condition import AliquotCondition
from .aliquot_type import AliquotType
from .receive import Receive


class Aliquot(BaseAliquot, SyncModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    receive = models.ForeignKey(
        Receive,
        editable=False)

    aliquot_type = models.ForeignKey(
        AliquotType,
        verbose_name="Aliquot Type",
        null=True)

    aliquot_condition = models.ForeignKey(
        AliquotCondition,
        verbose_name="Aliquot Condition",
        null=True,
        blank=True)

    is_rejected = models.BooleanField(
        verbose_name='rejected',
        default=False)

    objects = AliquotManager()

    history = SyncHistoricalRecords()

    def save(self, *args, **kwargs):
        self.subject_identifier = self.receive.registered_subject.subject_identifier
        super(Aliquot, self).save(*args, **kwargs)

    @property
    def specimen_identifier(self):
        return self.aliquot_identifier[:-4]

    @property
    def registered_subject(self):
        return self.receive.registered_subject

    @property
    def visit_code(self):
        return self.receive.visit

#     @property
#     def subject_visit(self):
#         MaternalVisit = models.get_model('maternal', 'MaternalVisit')
#         try:
#             return MaternalVisit.objects.get(
#                 appointment__visit_definition__code=self.visit_code,
#                 appointment__registered_subject=self.registered_subject)
#         except MaternalVisit.DoesNotExist:
#             return None
# 
#     @property
#     def subject_requisition(self):
#         model = self.receive.requisition_model_name
#         RequisitionModel = models.get_model('mb_lab', model)
#         try:
#             return RequisitionModel.objects.get(
#                 requisition_identifier=self.receive.requisition_identifier)
#         except RequisitionModel.DoesNotExist:
#             return None
# 
#     @property
#     def optional_description(self):
#         """See PackingListHelper."""
#         try:
#             return self.subject_requisition.optional_description
#         except AttributeError:
#             return None
# 
#     def processing(self):
#         url = reverse('admin:mb_lab_aliquotprocessing_add')
#         return '<a href="{0}?aliquot={1}">process</a>'.format(url, self.pk)
#     processing.allow_tags = True
# 
#     def related(self):
#         url = reverse('admin:mb_lab_aliquot_changelist')
#         return '<a href="{0}?q={1}">related</a>'.format(url, self.receive.receive_identifier)
#     related.allow_tags = True

    class Meta:
        app_label = 'td_lab'
        unique_together = (('receive', 'count'), )
