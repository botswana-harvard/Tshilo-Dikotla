# from django.db import models
# 
# from edc_base.model.models import BaseUuidModel
# from edc_constants.constants import NOT_APPLICABLE
# from edc_export.models import ExportTrackingFieldsMixin
# from edc_lab.lab_packing.models import BasePackingListItem
# from edc_registration.models import RegisteredSubject
# from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
# 
# from td.constants import INFANT
# 
# from .aliquot import Aliquot
# from .infant_requisition import InfantRequisition
# from .maternal_requisition import MaternalRequisition
# from .packing_list import PackingList
# from .panel import Panel
# 
# from ..managers import PackingListItemManager
# 
# 
# class PackingListItem(BasePackingListItem, SyncModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):
# 
#     packing_list = models.ForeignKey(PackingList, null=True)
# 
#     panel = models.ForeignKey(
#         Panel,
#         null=True,
#         blank=True)
# 
#     objects = PackingListItemManager()
# 
#     history = SyncHistoricalRecords()
# 
#     def get_subject_type(self):
#         aliquot = Aliquot.objects.get(aliquot_identifier=self.item_reference)
#         registered_subject = RegisteredSubject.objects.get(subject_identifier=aliquot.subject_identifier)
#         return registered_subject.subject_type
# 
#     def save(self, *args, **kwargs):
#         if self.item_reference:
#             aliquot = Aliquot.objects.get(aliquot_identifier=self.item_reference)
#             if self.get_subject_type() == INFANT:
#                 requisition = InfantRequisition.objects.get(
#                     requisition_identifier=aliquot.receive.requisition_identifier)
#             else:
#                 requisition = MaternalRequisition.objects.get(
#                     requisition_identifier=aliquot.receive.requisition_identifier)
#             self.panel = requisition.panel
#             self.item_priority = requisition.priority
#         super(PackingListItem, self).save(*args, **kwargs)
# 
#     def drawn_datetime(self):
#         retval = NOT_APPLICABLE
#         if self.item_reference:
#             aliquot = Aliquot.objects.get(aliquot_identifier=self.item_reference)
#             if self.get_subject_type() == INFANT:
#                 requisition = InfantRequisition.objects.get(
#                     requisition_identifier=aliquot.receive.requisition_identifier)
#             else:
#                 requisition = MaternalRequisition.objects.get(
#                     requisition_identifier=aliquot.receive.requisition_identifier)
#             retval = requisition.drawn_datetime
#         return retval
# 
#     def clinician(self):
#         retval = NOT_APPLICABLE
#         if self.item_reference:
#             aliquot = Aliquot.objects.get(aliquot_identifier=self.item_reference)
#             if self.get_subject_type() == INFANT:
#                 requisition = InfantRequisition.objects.get(
#                     requisition_identifier=aliquot.receive.requisition_identifier)
#             else:
#                 requisition = MaternalRequisition.objects.get(
#                     requisition_identifier=aliquot.receive.requisition_identifier)
#             retval = requisition.user_created
#         return retval
# 
#     def gender(self):
#         retval = NOT_APPLICABLE
#         if self.item_reference:
#             aliquot = Aliquot.objects.get(aliquot_identifier=self.item_reference)
#             registered_subject = RegisteredSubject.objects.get(subject_identifier=aliquot.subject_identifier)
#             retval = registered_subject.gender
#         return retval
# 
#     def natural_key(self):
#         return (self.item_reference, )
# 
#     class Meta:
#         app_label = "td_lab"
#         verbose_name = 'Packing List Item'
