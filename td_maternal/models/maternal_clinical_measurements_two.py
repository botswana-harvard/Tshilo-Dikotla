from django.db import models

from .base_maternal_clinical_measurements import BaseMaternalClinicalMeasurements


class MaternalClinicalMeasurementsTwo(BaseMaternalClinicalMeasurements):

    objects = models.Manager()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Maternal Clinical Measurements Two'
        verbose_name_plural = 'Maternal Clinical Measurements Two'
