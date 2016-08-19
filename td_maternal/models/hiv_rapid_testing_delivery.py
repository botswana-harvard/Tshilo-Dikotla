from .rapid_testing_mixin import RapidTestMixin
from .maternal_crf_model import MaternalCrfModel


class RapidTestingDelivery(MaternalCrfModel, RapidTestMixin):
    
    class Meta:
        app_label = 'td_maternal'
        verbose_name = "HIV Rapid Testing Delivery"
        verbose_name_plural = "HIV Rapid Testing Deliveries"