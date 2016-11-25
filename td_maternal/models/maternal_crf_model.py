from django.db import models

from edc_base.model.models import BaseUuidModel, UrlMixin
from edc_consent.model_mixins import RequiresConsentMixin
from edc_export.model_mixins import ExportTrackingFieldsMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_visit_tracking.model_mixins import CrfModelMixin
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin

from ..managers import VisitCrfModelManager

from .maternal_visit import MaternalVisit


class MaternalCrfModel(CrfModelMixin, ExportTrackingFieldsMixin, OffstudyMixin,
                       RequiresConsentMixin, UpdatesCrfMetadataModelMixin, UrlMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`MaternalVisit`). """

    maternal_visit = models.OneToOneField(MaternalVisit)

    objects = VisitCrfModelManager()

    def __str__(self):
        return "{}: {}".format(self.__class__._meta.model_name,
                               self.maternal_visit.appointment.subject_identifier)

    def natural_key(self):
        return self.maternal_visit.natural_key()

    class Meta:
        consent_model = 'td_maternal.maternalconsent'
        abstract = True
