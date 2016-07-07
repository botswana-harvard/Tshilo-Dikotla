from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
# from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_constants.choices import YES_NO, YES_NO_NA

from tshilo_dikotla.apps.td.choices import HOSPITALIZATION_REASON

from tshilo_dikotla.apps.td.choices import LAUGH, ENJOYMENT, BLAME, UNHAPPY, ANXIOUS, SAD, PANICK, TOP, CRYING, HARM

from .maternal_crf_model import MaternalCrfModel
from .diagnoses_mixin import DiagnosesMixin
from tshilo_dikotla.apps.td_list.models import MaternalHospitalization


class MaternalPostPartumFu(MaternalCrfModel, DiagnosesMixin):

    hospitalized = models.CharField(
        max_length=25,
        verbose_name="Has the mother been hospitalized since delivery?",
        choices=YES_NO,
        help_text="If No, end here.",
    )

    hospitalization_reason = models.ManyToManyField(
        MaternalHospitalization,
        verbose_name="Was the hospitalization for any of the following reasons?",
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
        verbose_name="How many days was the mother hospitalized?",
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
    )

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Post Partum Fu"
        verbose_name_plural = "Maternal Post Partum Fu"
