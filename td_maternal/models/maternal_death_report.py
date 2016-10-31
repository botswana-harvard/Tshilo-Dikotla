from django.db import models

# from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_death_report.model_mixins import DeathReportModelMixin
from edc_export.models import ExportTrackingFieldsMixin
# from edc_meta_data.managers import CrfMetaDataManager
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.model_mixins import CrfModelMixin

from .maternal_visit import MaternalVisit
from edc_base.model.models.url_mixin import UrlMixin


class MaternalDeathReport(CrfModelMixin, SyncModelMixin, DeathReportModelMixin,
                          ExportTrackingFieldsMixin, UrlMixin, BaseUuidModel):

    """ A model completed by the user on the mother's death. """

    maternal_visit = models.OneToOneField(MaternalVisit)

#     history = AuditTrail()

#     entry_meta_data_manager = CrfMetaDataManager(MaternalVisit)

    def natural_key(self):
        return self.maternal_visit.natural_key()
    natural_key.dependencies = ['td_maternal.maternalvisit']

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Death Report"
