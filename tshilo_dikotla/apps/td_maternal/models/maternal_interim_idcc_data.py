from django.db import models

# from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO

from .maternal_crf_model import MaternalCrfModel


class MaternalInterimIdcc(MaternalCrfModel):

    info_since_lastvisit = models.CharField(
        max_length=25,
        verbose_name="Is there new laboratory information available on the mother since last visit",
        choices=YES_NO,
        help_text="",)

    recent_cd4 = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Most recent CD4 available",
        help_text="",)

    recent_cd4_date = models.DateField(
        verbose_name="Date of recent CD4",
        blank=True,
        null=True)

    recent_vl = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Most recent VL available",
        help_text="",)

    recent_vl_date = models.DateField(
        verbose_name="Date of recent VL",
        blank=True,
        null=True)

    recent_hepb = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Most recent Hep B sAg available",
        help_text="",)

    recent_hepb_date = models.DateField(
        verbose_name="Date of recent Hep B",
        blank=True,
        null=True)

    recent_hepc = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Most recent Hep C Ab available",
        help_text="",)

    recent_hepc_date = models.DateField(
        verbose_name="Date of recent Hep C",
        blank=True,
        null=True)


#     history = AuditTrail()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Interim Idcc Data"
        verbose_name_plural = "Maternal Interim Idcc Data"
