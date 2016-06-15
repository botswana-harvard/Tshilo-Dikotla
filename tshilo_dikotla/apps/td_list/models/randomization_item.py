from edc_base.model.models import BaseListModel


class RandomizationItem (BaseListModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Randomization Item"
        verbose_name_plural = "Maternal Randomization Item"
