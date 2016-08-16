from edc_base.model.models import ListModelMixin
from edc_base.model.models import BaseUuidModel


class AutopsyInfoSource (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Autopsy Info Source"
        verbose_name_plural = "Autopsy Info Source"
