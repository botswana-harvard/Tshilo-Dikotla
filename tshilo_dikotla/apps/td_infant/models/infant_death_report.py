from django.db import models

from edc_registration.models import RegisteredSubject
# from edc_base.audit_trail import AuditTrail
from edc_death_report.models import DeathReportModelMixin, InfantDrugRelationshipMixin

from .infant_crf_model import InfantCrfModel


class InfantDeathReport (DeathReportModelMixin, InfantDrugRelationshipMixin, InfantCrfModel):

    """ A model completed by the user after an infant's death. """

    registered_subject = models.OneToOneField(RegisteredSubject)

#     history = AuditTrail()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Death Report"
