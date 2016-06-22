from edc_base.model.models import BaseListModel


class Malformations(BaseListModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Fetal Malformations"
        verbose_name_plural = "Fetal Malformations"
