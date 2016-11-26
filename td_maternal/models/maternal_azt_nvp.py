from django.db import models

# from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO

# from td.choices import AZT_NVP

from .maternal_crf_model import MaternalCrfModel


class MaternalAztNvp(MaternalCrfModel):

    azt_nvp_delivery = models.CharField(
        max_length=25,
        verbose_name="Please check if Nevirapine prophylaxis was given to the delivery site.",
        choices=YES_NO,
        help_text="",
    )

    date_given = models.DateField(
        verbose_name="Date given",
    )

    instructions_given = models.CharField(
        max_length=25,
        verbose_name="Were instructions given to the mother on administration of the medications?",
        choices=YES_NO,
        help_text="",
    )

    class Meta(MaternalCrfModel.Meta):
        app_label = 'td_maternal'
        verbose_name = "Maternal Azt Nvp"
        verbose_name_plural = "Maternal Azt Nvp"
