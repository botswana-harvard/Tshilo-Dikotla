from django.db import models

# from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_code_lists.models import WcsDxAdult

from tshilo_dikotla.apps.td.choices import DIAGNOSES

from .maternal_crf_model import MaternalCrfModel


class MaternalDiagnoses(MaternalCrfModel):

    instructions_given = models.CharField(
        max_length=25,
        verbose_name="Have there been any new diagnoses or medical problems in the mother's health since last visit?",
        choices=YES_NO,
        help_text="If No, skip next question.",
    )

    diagnoses = models.CharField(
        max_length=25,
        verbose_name="Have any of the following diagnoses occured since last visit?",
        choices=DIAGNOSES,
        help_text="",
    )

    diagnoses_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    has_who_dx = models.CharField(
        verbose_name=(
            "During this pregnancy, did the mother have any new diagnoses "
            "listed in the WHO Adult/Adolescent HIV clinical staging document which "
            "is/are NOT reported?"),
        max_length=3,
        choices=YES_NO_NA)

    who = models.ManyToManyField(
        WcsDxAdult,
        verbose_name="List any new WHO Stage III/IV diagnoses that are not reported in Question ?? above:")

#     history = AuditTrail()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Diagnoses"
        verbose_name_plural = "Maternal Diagnoses"
