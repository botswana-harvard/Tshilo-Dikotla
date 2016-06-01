from django.db import models
# from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_constants.choices import YES_NO, YES_NO_NA

from tshilo_dikotla.apps.td.choices import HOSPITALIZATION_REASON

from .maternal_crf_model import MaternalCrfModel
from .diagnoses_mixin import DiagnosesMixin


class MaternalPostPartumFu(MaternalCrfModel, DiagnosesMixin):

    hospitalized = models.CharField(
        max_length=25,
        verbose_name="Has the mother been hospitalized since delivery?",
        choices=YES_NO,
        help_text="If No, end here.",
    )

    hospitalization_reason = models.CharField(
        max_length=100,
        verbose_name="Was the hospitalization for any of the following reasons?",
        choices=HOSPITALIZATION_REASON,
        blank=True,
        null=True,
        help_text="",
    )

    hospitalization_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    hospitalization_days = models.IntegerField(
        verbose_name="Was the hospitalization for any of the following reasons?",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Post Partum Fu"
        verbose_name_plural = "Maternal Post Partum Fu"
