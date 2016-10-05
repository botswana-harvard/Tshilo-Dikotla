from edc_base.model.models import BaseUuidModel
from edc_metadata.model_mixins import CrfMetadataModelMixin


class CrfMetadata(CrfMetadataModelMixin, BaseUuidModel):

    def custom_post_update_crf_meta_data(self):
        """Custom methods that manipulate meta data on the post save.

        This method is called in the edc_meta_data signal."""
        pass

    class Meta:
        app_label = 'td_maternal'
