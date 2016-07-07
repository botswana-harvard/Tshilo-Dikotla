from edc_base.model.models import ListModelMixin


class MaternalRelatives(ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Relatives"
        verbose_name_plural = "Maternal Relatives"
