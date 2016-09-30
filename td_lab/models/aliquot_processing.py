# from django.db import models
# 
# from edc_base.model.models import BaseUuidModel
# from edc_export.models import ExportTrackingFieldsMixin
# from edc_lab.lab_aliquot.managers import AliquotProcessingManager
# from edc_lab.lab_aliquot.model_mixins import AliquotProcessingModelMixin
# from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
# 
# from .aliquot import Aliquot
# from .aliquot_profile import AliquotProfile
# 
# 
# class AliquotProcessing(AliquotProcessingModelMixin, SyncModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):
# 
#     aliquot = models.ForeignKey(
#         Aliquot,
#         verbose_name='Source Aliquot',
#         help_text='Create aliquots from this one.')
# 
#     profile = models.ForeignKey(
#         AliquotProfile,
#         verbose_name='Profile',
#         help_text='Create aliquots according to this profile.')
# 
#     objects = AliquotProcessingManager()
# 
#     history = SyncHistoricalRecords()
# 
#     def natural_key(self):
#         return self.aliquot.natural_key() + self.profile.natural_key()
# 
#     def deserialize_get_missing_fk(self, attrname):
#         retval = None
#         return retval
# 
#     class Meta:
#         app_label = 'td_lab'
