from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO

from .infant_crf_model import InfantCrfModel


class InfantFu(InfantCrfModel):

    """ A model completed by the user on the infant's follow up. """

    physical_assessment = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was physical assessment done today?",
        help_text="",
    )

    diarrhea_illness = models.CharField(
        verbose_name="Since the last scheduled visit, has the infant had any diarrheal illness "
                     "(at least 3 loose stools per day which is ALSO a change from the normal)",
        max_length=3,
        choices=YES_NO,
        help_text="Must be of grade 3 or 4",
    )

    has_dx = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Since the last attended scheduled visit, has the infant had any diagnosis that were NEW events",
        help_text="\'NEW events\' are those that were never previously reported OR a NEW "
                  "episode of a previously resolved diagnosis",
    )

    was_hospitalized = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Has the child been hospitalized overnight since the last scheduled visit "
                     "(or since discharge after birth,if this is the randomization visit)?",
        help_text="If 'Yes', the primary diagnosis(es) associated with the hospitalization(s) "
                  "must be recorded in follow up diagnoses section.",
    )

    days_hospitalized = models.IntegerField(
        verbose_name="If 'Yes', total number of days of hospitalization since the last scheduled visit.",
        help_text="",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(90), ],
    )

#     history = AuditTrail()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant FollowUp"
        verbose_name_plural = "Infant FollowUp"
