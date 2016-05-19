from edc_base.model.models import BaseListModel


class MaternalMedications (BaseListModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Medications"
        verbose_name_plural = "Maternal Medications"
