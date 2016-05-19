from edc_base.model.models import BaseListModel


class AutopsyInfoSource (BaseListModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Autopsy Info Source"
        verbose_name_plural = "Autopsy Info Source"
