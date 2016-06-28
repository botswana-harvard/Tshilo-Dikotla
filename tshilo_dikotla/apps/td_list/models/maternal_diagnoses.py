from edc_base.model.models import BaseListModel


class MaternalDiagnoses(BaseListModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Diagnoses"
        verbose_name_plural = "Maternal Diagnoses"