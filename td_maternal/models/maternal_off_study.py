from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_export.model_mixins import ExportTrackingFieldsMixin
# from edc_meta_data.managers import CrfMetaDataManager
from edc_offstudy.model_mixins import OffstudyModelMixin
from edc_visit_tracking.model_mixins import CrfModelMixin
from .maternal_crf_model import MaternalCrfModel

from .maternal_consent import MaternalConsent
from .maternal_visit import MaternalVisit


class MaternalOffStudy(MaternalCrfModel, OffstudyModelMixin):

    """ A model completed by the user on the visit when the mother is taken off-study. """

    consent_model = MaternalConsent

    visit_model = MaternalVisit

    maternal_visit = models.OneToOneField(MaternalVisit)

    @property
    def visit_model(self):
        return MaternalVisit

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Off Study"
