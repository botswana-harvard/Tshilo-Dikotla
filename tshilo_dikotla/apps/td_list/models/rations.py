from edc_base.model.models import ListModelMixin


class Rations (ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Rations"
        verbose_name_plural = "Rations"
