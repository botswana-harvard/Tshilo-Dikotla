from django.db import models

from edc_base.model.models import BaseUuidModel, UrlMixin
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_visit_tracking.managers import CrfModelManager
from edc_visit_tracking.model_mixins import CrfModelMixin, PreviousVisitModelMixin

from .maternal_visit import MaternalVisit


class MaternalCrfModel(CrfModelMixin, OffstudyMixin,
                       RequiresConsentMixin, PreviousVisitModelMixin,
                       UpdatesCrfMetadataModelMixin, UrlMixin, BaseUuidModel):

    """Model mixin for all Maternal CRF models."""

    maternal_visit = models.OneToOneField(MaternalVisit)

    objects = CrfModelManager()

    def natural_key(self):
        return self.maternal_visit.natural_key()
    natural_key.dependencies = ['td_maternal.maternalvisit']

    class Meta:
        abstract = True
        consent_model = 'td_maternal.maternalconsent'
