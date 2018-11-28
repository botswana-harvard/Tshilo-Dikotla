from edc_constants.choices import (NORMAL_ABNORMAL,
                                   YES_NO_NOT_EVALUATED_NA, NORMAL_ABNORMAL_NOEXAM)
from edc_constants.constants import NOT_APPLICABLE

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .infant_crf_model import InfantCrfModel


class InfantFuPhysical(InfantCrfModel):

    """ A model completed by the user on the infant's Infant follow up physical assessment. """

    weight_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Weight ",
        help_text="Please measure twice and enter the average of the two. Measured in kg.",
        validators=[MinValueValidator(0), MaxValueValidator(20.0), ],
    )

    height = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Height ",
        help_text="Please measure twice and enter the average of the two. Measured in centimeters, (cm)",
        validators=[MinValueValidator(0), MaxValueValidator(125), ],
    )

    head_circumference = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="What was the head circumference in centimeters? ",
        help_text="Please measure twice and enter the average of the two. Measured in centimeters, (cm)",
        validators=[MinValueValidator(0), MaxValueValidator(52.0), ],
    )

    general_activity = models.CharField(
        max_length=15,
        choices=NORMAL_ABNORMAL,
        verbose_name="General Activity? ",
        help_text="Report general activity ON THE DAY of the exam.")

    abnormal_activity = models.CharField(
        verbose_name="If abnormal (specify)",
        max_length=100,
        blank=True,
        null=True)

    physical_exam_result = models.CharField(
        max_length=15,
        choices=NORMAL_ABNORMAL_NOEXAM,
        verbose_name="What was the result of the Physical Exam? ",
        help_text="")

    heent_exam = models.CharField(
        max_length=15,
        choices=YES_NO_NOT_EVALUATED_NA,
        verbose_name="Was HEENT Exam Normal? ",
        default=NOT_APPLICABLE,
        help_text="")

    heent_no_other = models.TextField(
        verbose_name="If abnormal or not evaluated, specify",
        blank=True,
        null=True)

    resp_exam = models.CharField(
        max_length=15,
        choices=YES_NO_NOT_EVALUATED_NA,
        verbose_name="Was Respiratory Exam Normal?",
        default=NOT_APPLICABLE,
        help_text="")

    resp_exam_other = models.TextField(
        verbose_name="If abnormal or not evaluated, specify",
        blank=True,
        null=True)

    cardiac_exam = models.CharField(
        max_length=15,
        choices=YES_NO_NOT_EVALUATED_NA,
        verbose_name="Was Cardiac Exam Normal?",
        default=NOT_APPLICABLE,
        help_text="")

    cardiac_exam_other = models.TextField(
        verbose_name="If abnormal or not evaluated,(specify)",
        blank=True,
        null=True)

    abdominal_exam = models.CharField(
        max_length=15,
        choices=YES_NO_NOT_EVALUATED_NA,
        default=NOT_APPLICABLE,
        verbose_name="Was Abdominal Exam Normal?",
        help_text="")

    abdominal_exam_other = models.TextField(
        verbose_name="If abnormal or not evaluated, specify",
        blank=True,
        null=True)

    skin_exam = models.CharField(
        max_length=15,
        choices=YES_NO_NOT_EVALUATED_NA,
        verbose_name="Was Skin Exam Normal?",
        help_text="",
        default=NOT_APPLICABLE,)

    skin_exam_other = models.TextField(
        verbose_name="If abnormal or not evaluated, specify",
        help_text="",
        blank=True,
        null=True)

    neurologic_exam = models.CharField(
        max_length=15,
        choices=YES_NO_NOT_EVALUATED_NA,
        verbose_name="Was Neurological Exam Normal?",
        default=NOT_APPLICABLE,
        help_text="")

    neuro_exam_other = models.TextField(
        verbose_name="If abnormal or not evaluated, specify",
        blank=True,
        null=True)

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant FollowUp: Physical"
        verbose_name_plural = "Infant FollowUp: Physical"
