from django.db import models

from edc_death_report.model_mixins import DeathReportModelMixin
from edc_death_report.models import InfantDrugRelationshipMixin
from td_registration.models import RegisteredSubject

from .infant_crf_model import InfantCrfModel


class InfantDeathReport (DeathReportModelMixin, InfantDrugRelationshipMixin, InfantCrfModel):

    """ A model completed by the user after an infant's death. """

    registered_subject = models.OneToOneField(RegisteredSubject)

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Death Report"
