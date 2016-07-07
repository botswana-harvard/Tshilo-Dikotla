from edc_base.model.models import ListModelMixin


class InfantVaccines (ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Infant Vaccines"
        verbose_name_plural = "Infant Vaccines"
