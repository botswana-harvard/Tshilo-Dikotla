from django.db import models
from django.apps import apps

from edc_base.model.models import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_export.models import ExportTrackingFieldsMixin
from edc_offstudy.model_mixins import OffStudyMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_visit_tracking.model_mixins import CrfModelMixin
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin

# from ..managers import VisitCrfModelManager

from .maternal_consent import MaternalConsent
from .maternal_visit import MaternalVisit
from .maternal_off_study import MaternalOffStudy
from django.urls.base import reverse


class MaternalCrfModel(SyncModelMixin, CrfModelMixin, ExportTrackingFieldsMixin, OffStudyMixin,
                       RequiresConsentMixin, UpdatesCrfMetadataModelMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`MaternalVisit`). """

    visit_model_attr = 'maternal_visit'

    off_study_model = ('td_maternal', 'MaternalOffStudy')

    maternal_visit = models.OneToOneField(MaternalVisit)

    history = SyncHistoricalRecords()

#     objects = VisitCrfModelManager()
#     @property
#     def off_study_model(self):
#         return MaternalOffStudy
    def is_off_study_on_previous_visit_or_raise(self):
        pass

    def is_off_study_or_raise(self):
        pass

    def has_off_study_report_or_raise(self, subject_identifier, report_date):
        pass

    def __str__(self):
        return "{}: {}".format(self.__class__._meta.model_name,
                               self.maternal_visit.appointment.subject_identifier)

    def natural_key(self):
        return self.maternal_visit.natural_key()

    class Meta:
        consent_model = 'td_maternal.maternalconsent'
        abstract = True
