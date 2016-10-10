from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_metadata.model_mixins import RequisitionMetadataModelMixin


class RequisitionMetadata(RequisitionMetadataModelMixin, BaseUuidModel):

    class Meta(RequisitionMetadataModelMixin.Meta):
        app_label = 'td_maternal'
