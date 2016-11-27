from django.db import models

from edc_base.model.models import BaseUuidModel, UrlMixin

from edc_base.model.models import HistoricalRecords
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_visit_tracking.model_mixins import CrfModelMixin

from ..managers import InfantVisitCrfManager

from .infant_visit import InfantVisit


class InfantCrfModel(CrfModelMixin, OffstudyMixin,
                     UpdatesCrfMetadataModelMixin, UrlMixin, BaseUuidModel):

    """ A model completed by the user on the infant's scheduled visit. """

    infant_visit = models.OneToOneField(InfantVisit)

    objects = InfantVisitCrfManager()

    history = HistoricalRecords()

    def __str__(self):
        return "{}: {}".format(self.__class__._meta.model_name,
                               self.infant_visit.appointment.subject_identifier)

    def get_consenting_subject_identifier(self):
        """Returns mother's identifier."""
        return self.get_visit().appointment.registered_subject.relative_identifier

    class Meta:
        abstract = True
