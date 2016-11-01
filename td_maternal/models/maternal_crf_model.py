from django.db import models

from edc_base.model.models import BaseUuidModel, UrlMixin
from edc_consent.model_mixins import RequiresConsentMixin
from edc_export.models import ExportTrackingFieldsMixin
from edc_offstudy.model_mixins import OffStudyMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_visit_tracking.model_mixins import CrfModelMixin
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin

# from ..managers import VisitCrfModelManager

from .maternal_visit import MaternalVisit


class MaternalCrfModel(SyncModelMixin, CrfModelMixin, ExportTrackingFieldsMixin, OffStudyMixin,
                       RequiresConsentMixin, UpdatesCrfMetadataModelMixin, UrlMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`MaternalVisit`). """

    off_study_model = ('td_maternal', 'MaternalOffStudy')

    maternal_visit = models.OneToOneField(MaternalVisit)

    history = SyncHistoricalRecords()

    def is_off_study_on_previous_visit_or_raise(self):
        pass

    def is_off_study_or_raise(self):
        pass

    @classmethod
    def visit_model_attr(cls):
        return 'maternal_visit'

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
