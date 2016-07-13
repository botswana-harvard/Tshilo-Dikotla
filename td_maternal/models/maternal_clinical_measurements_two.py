from django.db import models

from ..managers import MaternalClinicalMeasurementsTwoManager
from .base_maternal_clinical_measurements import BaseMaternalClinicalMeasurements


class MaternalClinicalMeasurementsTwo(BaseMaternalClinicalMeasurements):

    objects = MaternalClinicalMeasurementsTwoManager()
    
    def __str__(self):
        return "{0}".format(self.registered_subject.subject_identifier)

    def natural_key(self):
        return self.registered_subject.natural_key()
    natural_key.dependencies = ['edc_registration.registeredsubject']

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Maternal Clinical Measurements Two'
        verbose_name_plural = 'Maternal Clinical Measurements Two'
