from django.db import models

from edc_meta_data.managers import CrfMetaDataManager
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin
from edc_export.models import ExportTrackingFieldsMixin
from edc_offstudy.models import OffStudyMixin
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfModelMixin

from .maternal_consent import MaternalConsent
from .maternal_visit import MaternalVisit


class MaternalCrfModel(CrfModelMixin, ExportTrackingFieldsMixin, SyncModelMixin, OffStudyMixin,
                       RequiresConsentMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`MaternalVisit`). """

    consent_model = MaternalConsent

    visit_model_attr = 'maternal_visit'

    off_study_model = ('td_maternal', 'MaternalOffStudy')

    maternal_visit = models.OneToOneField(MaternalVisit)

    history = AuditTrail()

    entry_meta_data_manager = CrfMetaDataManager(MaternalVisit)

    class Meta:
        abstract = True
