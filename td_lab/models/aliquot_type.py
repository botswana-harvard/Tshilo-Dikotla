from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_lab.lab_aliquot.model_mixins import AliquotTypeModelMixin
from edc_lab.lab_aliquot.managers import AliquotTypeManager


class AliquotType(AliquotTypeModelMixin, BaseUuidModel):

    objects = AliquotTypeManager()

    class Meta:
        app_label = 'td_lab'
        ordering = ["name"]
