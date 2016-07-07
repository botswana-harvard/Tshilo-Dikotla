from edc_base.model.models import ListModelMixin


class ChronicConditions(ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Chronic Conditions"
        verbose_name_plural = "Chronic Conditions"
