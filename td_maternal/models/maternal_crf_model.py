from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_export.models import ExportTrackingFieldsMixin
from edc_offstudy.model_mixins import OffStudyMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_visit_tracking.model_mixins import CrfModelMixin

# from ..managers import VisitCrfModelManager

from .maternal_consent import MaternalConsent
from .maternal_visit import MaternalVisit


class MaternalCrfModel(SyncModelMixin, CrfModelMixin, ExportTrackingFieldsMixin, OffStudyMixin,
                       RequiresConsentMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`MaternalVisit`). """

    consent_model = MaternalConsent

    visit_model_attr = 'maternal_visit'

    off_study_model = ('td_maternal', 'MaternalOffStudy')

    maternal_visit = models.OneToOneField(MaternalVisit)

    history = SyncHistoricalRecords()

#     objects = VisitCrfModelManager()

    def __str__(self):
        return "{}: {}".format(self.__class__._meta.model_name,
                               self.maternal_visit.appointment.registered_subject.subject_identifier)

    def natural_key(self):
        return self.maternal_visit.natural_key()

    class Meta:
        abstract = True
