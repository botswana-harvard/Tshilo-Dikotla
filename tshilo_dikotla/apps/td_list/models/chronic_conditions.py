from edc_base.model.models import BaseListModel


class ChronicConditions (BaseListModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Chronic Conditions"
        verbose_name_plural = "Chronic Conditions"
