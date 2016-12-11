
from .diagnosis_mixin import DiagnosisMixin
from .maternal_crf_model import MaternalCrfModel


class MaternalDiagnosis(DiagnosisMixin, MaternalCrfModel):

    class Meta(MaternalCrfModel.Meta):
        app_label = 'td_maternal'
        verbose_name = "Maternal Diagnosis"
        verbose_name_plural = "Maternal Diagnoses"
