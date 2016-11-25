
from .maternal_crf_model import MaternalCrfModel
from .diagnoses_mixin import DiagnosesMixin


class MaternalDiagnoses(MaternalCrfModel, DiagnosesMixin):

    class Meta(MaternalCrfModel.Meta):
        app_label = 'td_maternal'
        verbose_name = "Maternal Diagnoses"
        verbose_name_plural = "Maternal Diagnoses"
