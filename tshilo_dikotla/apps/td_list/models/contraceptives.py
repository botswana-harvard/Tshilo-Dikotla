from edc_base.model.models import BaseListModel


class Contraceptives (BaseListModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Contraceptives"
        verbose_name_plural = "Contraceptives"
