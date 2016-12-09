from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .base_maternal_clinical_measurements import BaseMaternalClinicalMeasurements


class MaternalClinicalMeasurementsOne(BaseMaternalClinicalMeasurements):

    ADMIN_SITE_NAME = 'td_maternal_admin'

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Mother's height? ",
        validators=[MinValueValidator(134), MaxValueValidator(195), ],
        help_text="Measured in Centimeters (cm)")

    class Meta(BaseMaternalClinicalMeasurements.Meta):
        app_label = 'td_maternal'
        verbose_name = 'Maternal Clinical Measurements One'
        verbose_name_plural = 'Maternal Clinical Measurements One'
