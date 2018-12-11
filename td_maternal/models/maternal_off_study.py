from edc_export.models import ExportTrackingFieldsMixin
from edc_meta_data.managers import CrfMetaDataManager
from edc_offstudy.models import OffStudyModelMixin
from edc_visit_tracking.models import CrfModelMixin

from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin

from .maternal_consent import MaternalConsent
from .maternal_visit import MaternalVisit


# from edc_base.audit_trail import AuditTrail
# from edc_sync.models import SyncModelMixin
class MaternalOffStudy(OffStudyModelMixin, CrfModelMixin,
                       RequiresConsentMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    """ A model completed by the user on the visit when the mother is taken off-study. """

    consent_model = MaternalConsent

    visit_model = MaternalVisit

    visit_model_attr = 'maternal_visit'

    maternal_visit = models.OneToOneField(MaternalVisit)

    entry_meta_data_manager = CrfMetaDataManager(MaternalVisit)

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Off Study"
