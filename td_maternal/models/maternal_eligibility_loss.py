from django.db import models
from django.utils import timezone

# from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_export.models import ExportTrackingFieldsMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords

from .maternal_eligibility import MaternalEligibility

from ..managers import MaternalEligibilityLossManager
from edc_base.model.models.url_mixin import UrlMixin


class MaternalEligibilityLoss(SyncModelMixin, ExportTrackingFieldsMixin, UrlMixin, BaseUuidModel):
    """ A model triggered and completed by system when a mother is in-eligible. """

    maternal_eligibility = models.OneToOneField(MaternalEligibility)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=timezone.now,
        help_text='Date and time of report.')

    reason_ineligible = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        help_text='Gets reasons from Maternal Eligibility.ineligibility')

    objects = MaternalEligibilityLossManager()

    history = SyncHistoricalRecords()

    def __str__(self):
        return "{0}".format(self.maternal_eligibility.eligibility_id)

    def natural_key(self):
        return self.maternal_eligibility.natural_key()

    def ineligibility(self):
        return self.reason_ineligible or []
    reason_ineligible.allow_tags = True

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Maternal Eligibility Loss'
        verbose_name_plural = 'Maternal Eligibility Loss'
