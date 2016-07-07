from edc_base.model.models import ListModelMixin


class Foods (ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Foods"
        verbose_name_plural = "Foods"
