from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_export.models import ExportTrackingFieldsMixin
# from edc_meta_data.managers import CrfMetaDataManager
from edc_offstudy.model_mixins import OffStudyMixin
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_visit_tracking.model_mixins import CrfModelMixin

from ..managers import InfantVisitCrfManager
from .infant_visit import InfantVisit


class InfantCrfModel(CrfModelMixin, SyncModelMixin, OffStudyMixin, ExportTrackingFieldsMixin,
                     UpdatesCrfMetadataModelMixin, BaseUuidModel):

    """ A model completed by the user on the infant's scheduled visit. """

    off_study_model = ('td_infant', 'InfantOffStudy')

    infant_visit = models.OneToOneField(InfantVisit)

    history = SyncHistoricalRecords()

    objects = InfantVisitCrfManager()
#     entry_meta_data_manager = CrfMetaDataManager(InfantVisit)

    def __str__(self):
        return "{}: {}".format(self.__class__._meta.model_name,
                               self.infant_visit.appointment.subject_identifier)

    def get_consenting_subject_identifier(self):
        """Returns mother's identifier."""
        return self.get_visit().appointment.registered_subject.relative_identifier

    def is_off_study_or_raise(self):
        pass

    def is_off_study_on_previous_visit_or_raise(self):
        pass

    @property
    def visit(self):
        return getattr(self, 'infant_visit')

    class Meta:
        abstract = True
