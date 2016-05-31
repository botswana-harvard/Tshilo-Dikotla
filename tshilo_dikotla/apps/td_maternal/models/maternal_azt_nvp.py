from django.db import models

# from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO

from tshilo_dikotla.apps.td.choices import AZT_NVP

from .maternal_crf_model import MaternalCrfModel


class MaternalAztNvp(MaternalCrfModel):

    azt_nvp = models.CharField(
        max_length=25,
        verbose_name="Please check which infant prophylaxis regiment the mother was given.",
        choices=AZT_NVP,
        help_text="",
    )

    date_given = models.DateField(
        verbose_name="Date given",
    )

    instructions_given = models.CharField(
        max_length=25,
        verbose_name="Where instructions given to the mother on administration of the medications?",
        choices=YES_NO,
        help_text="",
    )

#     history = AuditTrail()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Azt Nvp"
        verbose_name_plural = "Maternal Azt Nvp"
