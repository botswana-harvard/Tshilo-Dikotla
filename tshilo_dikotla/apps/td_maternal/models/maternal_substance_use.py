from .base_substance_use_mixin import BaseSubstanceUseMixin

from .maternal_crf_model import MaternalCrfModel

class MaternalSubstanceUse(BaseSubstanceUseMixin, MaternalCrfModel):

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Substance Use'
        verbose_name_plural = 'Substance Use'