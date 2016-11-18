from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_export.model_mixins import ExportTrackingFieldsMixin
from edc_base.model.models import HistoricalRecords

from edc_lab.model_mixins import SpecimenCollectionModelMixin, SpecimenCollectionItemModelMixin


class SpecimenCollection(SpecimenCollectionModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    history = HistoricalRecords()

    class Meta(SpecimenCollectionModelMixin.Meta):
        app_label = 'td_lab'


class SpecimenCollectionItem(SpecimenCollectionItemModelMixin,
                             ExportTrackingFieldsMixin, BaseUuidModel):

    specimen_collection = models.ForeignKey(SpecimenCollection)

    history = HistoricalRecords()

    class Meta(SpecimenCollectionItemModelMixin.Meta):
        app_label = 'td_lab'
