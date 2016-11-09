from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_export.models import ExportTrackingFieldsMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords

from edc_lab.specimen.model_mixins import SpecimenCollectionModelMixin, SpecimenCollectionItemModelMixin


class SpecimenCollection(SpecimenCollectionModelMixin, SyncModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    history = SyncHistoricalRecords()

    class Meta(SpecimenCollectionModelMixin.Meta):
        app_label = 'td_lab'


class SpecimenCollectionItem(SpecimenCollectionItemModelMixin, SyncModelMixin,
                             ExportTrackingFieldsMixin, BaseUuidModel):

    specimen_collection = models.ForeignKey(SpecimenCollection)

    history = SyncHistoricalRecords()

    class Meta(SpecimenCollectionItemModelMixin.Meta):
        app_label = 'td_lab'
