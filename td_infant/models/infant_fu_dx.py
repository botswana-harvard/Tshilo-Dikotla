from django.db import models

from edc_constants.choices import YES_NO
from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_visit_tracking.models import CrfInlineModelMixin

from tshilo_dikotla.choices import DX_INFANT

from ..managers import InfantFuDxItemsManager

from .infant_crf_model import InfantCrfModel


class InfantFuDx(InfantCrfModel):

    """ A model completed by the user on the infant's follow up dx. """

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant FollowUp: Dx"
        verbose_name_plural = "Infant FollowUp: Dx"


class InfantFuDxItems(CrfInlineModelMixin, SyncModelMixin, BaseUuidModel):

    infant_fu_dx = models.ForeignKey(InfantFuDx)

    fu_dx = models.CharField(
        verbose_name="Diagnosis",
        max_length=150,
        choices=DX_INFANT)

    fu_dx_specify = models.CharField(
        verbose_name="Diagnosis specification",
        max_length=50,
        blank=True,
        null=True)

    health_facility = models.CharField(
        verbose_name="Seen at health facility for Dx",
        choices=YES_NO,
        max_length=3)

    was_hospitalized = models.CharField(
        verbose_name="Hospitalized?",
        choices=YES_NO,
        max_length=3)

    objects = InfantFuDxItemsManager()

    history = SyncHistoricalRecords()

    def natural_key(self):
        return (self.fu_dx, ) + self.infant_fu_dx.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant FollowUp: Dx"
        unique_together = ('fu_dx', 'infant_fu_dx')
