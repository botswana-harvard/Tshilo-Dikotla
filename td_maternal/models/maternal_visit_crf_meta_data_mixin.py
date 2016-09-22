from edc_metadata.model_mixins import CreatesMetadataModelMixin


class MaternalVisitCrfMetaDataMixin(CreatesMetadataModelMixin):

    def custom_post_update_crf_meta_data(self):
        """Custom methods that manipulate meta data on the post save.

        This method is called in the edc_meta_data signal."""
        pass

    class Meta:
        abstract = True
