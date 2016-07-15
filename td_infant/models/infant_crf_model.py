from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_export.models import ExportTrackingFieldsMixin
from edc_meta_data.managers import CrfMetaDataManager
from edc_offstudy.models import OffStudyMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_visit_tracking.models import CrfModelMixin

from ..managers import InfantVisitCrfManager
from .infant_visit import InfantVisit


class InfantCrfModel(CrfModelMixin, SyncModelMixin, OffStudyMixin, ExportTrackingFieldsMixin,
                    BaseUuidModel):

    """ A model completed by the user on the infant's scheduled visit. """

    off_study_model = ('td_infant', 'InfantOffStudy')

    infant_visit = models.OneToOneField(InfantVisit)

    history = SyncHistoricalRecords()

    objects = InfantVisitCrfManager()
    entry_meta_data_manager = CrfMetaDataManager(InfantVisit)

    def get_consenting_subject_identifier(self):
        """Returns mother's identifier."""
        return self.get_visit().appointment.registered_subject.relative_identifier

    class Meta:
        abstract = True
