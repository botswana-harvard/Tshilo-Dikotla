from django.db import models

from edc_base.model.fields import OtherCharField
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_code_lists.models import WcsDxAdult

from td_list.models import MaternalDiagnoses


class DiagnosesMixin(models.Model):

    """Base Model for forms with diagnosis questions i.e Maternal Diagnoses, Maternal Post Partum Fu1 etc"""
    new_diagnoses = models.CharField(
        max_length=25,
        verbose_name="Have there been any new diagnoses or medical problems in the mother's health since last visit?",
        choices=YES_NO,
        help_text="",
    )

    diagnoses = models.ManyToManyField(
        MaternalDiagnoses,
        verbose_name="Have any of the following diagnoses occured since last visit?",
        blank=True,
        null=True,
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

    class Meta:
        abstract = True