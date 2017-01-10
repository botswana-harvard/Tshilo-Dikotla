from edc_base.model.models import BaseUuidModel
from edc_death_report.model_mixins import DeathReportModelMixin
from edc_death_report.models import InfantDrugRelationshipMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin

from ..managers import InfantDeathReportManager


class InfantDeathReport (DeathReportModelMixin, NonUniqueSubjectIdentifierFieldMixin,
                         InfantDrugRelationshipMixin, BaseUuidModel):

    """ A model completed by the user after an infant's death. """

    objects = InfantDeathReportManager()

    def natural_key(self):
        return (self.subject_identifier, )

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Death Report"
