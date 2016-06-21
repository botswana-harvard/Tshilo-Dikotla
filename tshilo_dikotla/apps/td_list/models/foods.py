from edc_base.model.models import BaseListModel


class Foods (BaseListModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Foods"
        verbose_name_plural = "Foods"
