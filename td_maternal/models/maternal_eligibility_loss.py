from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_base.model.models import HistoricalRecords
from edc_base.model.models.url_mixin import UrlMixin
from edc_base.utils import get_utcnow

from ..managers import MaternalEligibilityLossManager


class MaternalEligibilityLoss(UrlMixin, BaseUuidModel):
    """ A model triggered and completed by system when a mother is in-eligible. """

    maternal_eligibility_reference = models.UUIDField()

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=get_utcnow,
        help_text='Date and time of report.')

    reason_ineligible = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        help_text='Gets reasons from Maternal Eligibility.ineligibility')

    objects = MaternalEligibilityLossManager()

    history = HistoricalRecords()

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
