from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_lab.specimen.model_mixins import SpecimenCollectionModelMixin, SpecimenCollectionItemModelMixin


class SpecimenCollection(SpecimenCollectionModelMixin, BaseUuidModel):

    class Meta(SpecimenCollectionModelMixin.Meta):
        app_label = 'td_lab'


class SpecimenCollectionItem(SpecimenCollectionItemModelMixin, BaseUuidModel):

    specimen_collection = models.ForeignKey(SpecimenCollection)

    class Meta(SpecimenCollectionItemModelMixin.Meta):
        app_label = 'td_lab'
