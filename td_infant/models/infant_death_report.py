from edc_base.model.models import BaseUuidModel
from edc_death_report.model_mixins import DeathReportModelMixin
from edc_death_report.models import InfantDrugRelationshipMixin
from edc_registration.model_mixins import SubjectIdentifierModelMixin


class InfantDeathReport (DeathReportModelMixin, SubjectIdentifierModelMixin,
                         InfantDrugRelationshipMixin, BaseUuidModel):

    """ A model completed by the user after an infant's death. """

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Death Report"
