from django.db import models

from edc_base.model.models import BaseUuidModel, UrlMixin
from edc_export.model_mixins import ExportTrackingFieldsMixin
# from edc_meta_data.managers import CrfMetaDataManager
from edc_offstudy.model_mixins import OffstudyModelMixin
from edc_base.model.models import HistoricalRecords
from edc_visit_tracking.model_mixins import CrfModelMixin

from .infant_visit import InfantVisit


class InfantOffStudy(CrfModelMixin, OffstudyModelMixin, ExportTrackingFieldsMixin, UrlMixin, BaseUuidModel):

    """ A model completed by the user when the infant is taken off study. """

    infant_visit = models.OneToOneField(InfantVisit)

    history = HistoricalRecords()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Off-Study"
        verbose_name_plural = "Infant Off-Study"
