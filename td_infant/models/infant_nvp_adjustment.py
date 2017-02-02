from django.db import models

from edc_constants.choices import YES_NO, YES_NO_NA


from .infant_crf_model import InfantCrfModel


class InfantNvpAdjustment(InfantCrfModel):

    dose_adjustment = models.CharField(
        verbose_name='Was it necessary to adjust the infant’s dose of NVP prophylaxis at 2 weeks of life?',
        choices=YES_NO,
        help_text='If NO, skip to : Since discharge from the hospital...',
        max_length=3)

    adjusted_dose = models.CharField(
        verbose_name='If YES, please enter the dose adjusted by weight at 2 weeks of life.',
        help_text='mL',
        blank=True,
        null=True,
        max_length=10)

    dose_4_weeks = models.CharField(
        verbose_name='Since discharge from the hospital has the infant taken NVP prophylaxis daily for 4 weeks?',
        help_text='',
        choices=YES_NO_NA,
        max_length=3)

    incomplete_dose = models.CharField(
        verbose_name='If NO, please explain why.',
        help_text='',
        blank=True,
        null=True,
        max_length=50)

    class Meta():
        app_label = 'td_infant'
        verbose_name = 'Infant Nevirapine 2 Week Adjustment'
        verbose_name_plural = 'Infant Nevirapine 2 Week Adjustment'
