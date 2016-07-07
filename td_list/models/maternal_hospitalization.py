from edc_base.model.models import ListModelMixin


class MaternalHospitalization(ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Hospitalization"
        verbose_name_plural = "Maternal Hospitalizations"
