from edc_base.model.models import ListModelMixin


class Malformations(ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Fetal Malformations"
        verbose_name_plural = "Fetal Malformations"
