
from .base_maternal_clinical_measurements import BaseMaternalClinicalMeasurements


class MaternalClinicalMeasurementsTwo(BaseMaternalClinicalMeasurements):

    class Meta(BaseMaternalClinicalMeasurements.Meta):
        app_label = 'td_maternal'
        verbose_name = 'Maternal Clinical Measurements Two'
        verbose_name_plural = 'Maternal Clinical Measurements Two'
