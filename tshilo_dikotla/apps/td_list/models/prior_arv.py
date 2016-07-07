from edc_base.model.models import ListModelMixin


class PriorArv (ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Enroll: Prior Arv"
        verbose_name_plural = "Maternal Enroll: Prior Arv"
