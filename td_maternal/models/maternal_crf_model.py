from django.db import models

from edc_base.model.models import BaseUuidModel, UrlMixin
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_visit_tracking.managers import CrfModelManager
from edc_visit_tracking.model_mixins import CrfModelMixin, PreviousVisitModelMixin

from .maternal_visit import MaternalVisit


class TdCrfModelManager(CrfModelManager):

    def get_by_natural_key(self, maternal_visit):
        return self.get(**{self.model.visit_model_attr(): maternal_visit})


class MaternalCrfModel(CrfModelMixin, OffstudyMixin,
                       RequiresConsentMixin, PreviousVisitModelMixin,
                       UpdatesCrfMetadataModelMixin, UrlMixin, BaseUuidModel):

    """Model mixin for all Maternal CRF models."""

    ADMIN_SITE_NAME = 'td_maternal_admin'

    maternal_visit = models.OneToOneField(MaternalVisit)

    objects = TdCrfModelManager()

    def natural_key(self):
        return (self.maternal_visit, )
    natural_key.dependencies = ['td_maternal.maternalvisit']

    class Meta:
        abstract = True
        consent_model = 'td_maternal.maternalconsent'
