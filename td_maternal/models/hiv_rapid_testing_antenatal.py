from .rapid_testing_mixin import RapidTestMixin
from .maternal_crf_model import MaternalCrfModel


class RapidTestingAntenatal(MaternalCrfModel, RapidTestMixin):
    
    class Meta:
        app_label = 'td_maternal'
        verbose_name = "HIV Rapid Testing Antenatal"
        verbose_name_plural = "HIV Rapid Testing Antenatal"