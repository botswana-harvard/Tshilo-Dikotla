from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_export.models import ExportTrackingFieldsMixin
# from edc_meta_data.managers import CrfMetaDataManager
from edc_offstudy.model_mixins import OffStudyModelMixin
# from edc_sync.models import SyncModelMixin
from edc_visit_tracking.model_mixins import CrfModelMixin

from .maternal_consent import MaternalConsent
from .maternal_visit import MaternalVisit


class MaternalOffStudy(CrfModelMixin, OffStudyModelMixin,
                       RequiresConsentMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    """ A model completed by the user on the visit when the mother is taken off-study. """

    consent_model = MaternalConsent

    visit_model_attr = 'maternal_visit'

    maternal_visit = models.OneToOneField(MaternalVisit)

#     entry_meta_data_manager = CrfMetaDataManager(MaternalVisit)

    def is_off_study_on_previous_visit_or_raise(self):
        print(self.off_study_model.visit_model, "<><>><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><")
        #super().is_off_study_on_previous_visit_or_raise

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Off Study"
