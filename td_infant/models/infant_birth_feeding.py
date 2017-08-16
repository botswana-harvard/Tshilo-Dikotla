from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_visit_tracking.models import CrfInlineModelMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_export.models import ExportTrackingFieldsMixin

from tshilo_dikotla.choices import FEEDING_CHOICES

from ..choices import INFANT_VACCINATIONS
from ..managers import InfantVaccinesManager

from .infant_crf_model import InfantCrfModel


class InfantBirthFeedingVaccine(InfantCrfModel):

    """ A model completed by the user on the infant's feeding & vaccination/ immunization. """

    feeding_after_delivery = models.CharField(
        max_length=50,
        choices=FEEDING_CHOICES,
        verbose_name="How was the infant being fed immediately after delivery? ",
        help_text=" ...before discharge from maternity")

    comments = models.TextField(
        max_length=250,
        verbose_name="Comment if any additional pertinent information: ",
        blank=True,
        null=True)

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Birth Feeding & Vaccination"


class InfantVaccines(CrfInlineModelMixin, SyncModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    infant_birth_feed_vaccine = models.ForeignKey(InfantBirthFeedingVaccine)

    vaccination = models.CharField(
        choices=INFANT_VACCINATIONS,
        verbose_name="Since delivery, did the child receive any of the following vaccinations",
        max_length=100)

    vaccine_date = models.DateField(
        verbose_name='Date Vaccine was given',
        null=True,
        blank=True)

    objects = InfantVaccinesManager()

    history = SyncHistoricalRecords()

    def natural_key(self):
        return (self.vaccination, ) + self.infant_birth_feed_vaccine.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Vaccines"
        verbose_name_plural = "Infant Vaccines"
        unique_together = (
            'infant_birth_feed_vaccine', 'vaccination', 'vaccine_date')
