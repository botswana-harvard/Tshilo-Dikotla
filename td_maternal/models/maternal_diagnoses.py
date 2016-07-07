from django.db import models

# from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_code_lists.models import WcsDxAdult

from tshilo_dikotla.choices import DIAGNOSES

from .maternal_crf_model import MaternalCrfModel
from .diagnoses_mixin import DiagnosesMixin


class MaternalDiagnoses(MaternalCrfModel, DiagnosesMixin):

#     history = AuditTrail()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Diagnoses"
        verbose_name_plural = "Maternal Diagnoses"
