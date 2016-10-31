from django.db import models

from edc_base.model.models import BaseUuidModel, UrlMixin
from edc_export.models import ExportTrackingFieldsMixin
# from edc_meta_data.managers import CrfMetaDataManager
from edc_offstudy.model_mixins import OffStudyModelMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_visit_tracking.model_mixins import CrfModelMixin

from .infant_visit import InfantVisit


class InfantOffStudy(CrfModelMixin, SyncModelMixin, OffStudyModelMixin, ExportTrackingFieldsMixin, UrlMixin, BaseUuidModel):

    """ A model completed by the user when the infant is taken off study. """

    infant_visit = models.OneToOneField(InfantVisit)

    visit_model_attr = 'infant_visit'

    # entry_meta_data_manager = CrfMetaDataManager(InfantVisit)

    history = SyncHistoricalRecords()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Off-Study"
        verbose_name_plural = "Infant Off-Study"
