from edc_base.model.models import BaseListModel


class Rations (BaseListModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Rations"
        verbose_name_plural = "Rations"
