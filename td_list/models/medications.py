from edc_base.model.models import ListModelMixin


class MaternalMedications (ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Medications"
        verbose_name_plural = "Maternal Medications"
