from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from edc_registration.models import RegisteredSubject

from ..managers import MaternalClinicalMeasurementsOneManager
from .base_maternal_clinical_measurements import BaseMaternalClinicalMeasurements


class MaternalClinicalMeasurementsOne(BaseMaternalClinicalMeasurements):

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Mother's height? ",
        validators=[MinValueValidator(134), MaxValueValidator(195), ],
        help_text="Measured in Centimeters (cm)")

    objects = MaternalClinicalMeasurementsOneManager()
    
    def __str__(self):
        return "{0}".format(self.registered_subject.subject_identifier)

    def natural_key(self):
        return self.registered_subject.natural_key()
    natural_key.dependencies = ['edc_registration.registeredsubject']

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Maternal Clinical Measurements One'
        verbose_name_plural = 'Maternal Clinical Measurements One'