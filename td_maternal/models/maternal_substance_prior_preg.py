from django.db import models

from edc_constants.choices import YES_NO

from td_maternal.maternal_choices import SMOKING_DRINKING_FREQUENCY
from .maternal_crf_model import MaternalCrfModel


class MaternalSubstanceUsePriorPreg(MaternalCrfModel):

    smoked_prior_to_preg = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Has the participant ever smoked cigarettes prior to this pregnancy?",
        help_text="")

    smoking_prior_preg_freq = models.CharField(
        max_length=30,
        choices=SMOKING_DRINKING_FREQUENCY,
        verbose_name="If yes, please indicate how much: ",
        blank=True,
        null=True,
        help_text="")

    alcohol_prior_pregnancy = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Has the participant ever drank alcohol prior to this pregnancy?",
        help_text="")

    alcohol_prior_preg_freq = models.CharField(
        max_length=30,
        choices=SMOKING_DRINKING_FREQUENCY,
        verbose_name="If yes, please indicate how much: ",
        blank=True,
        null=True,
        help_text="")

    marijuana_prior_preg = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Has the participant ever used marijuana prior to this pregnancy?",
        help_text="")

    marijuana_prior_preg_freq = models.CharField(
        max_length=30,
        choices=SMOKING_DRINKING_FREQUENCY,
        verbose_name="If yes, please indicate how much: ",
        blank=True,
        null=True,
        help_text="")

    other_illicit_substances_prior_preg = models.CharField(
        max_length=500,
        verbose_name="Please list any other illicit substances that the participant reports using prior to this pregnancy.",
        blank=True,
        null=True,
        help_text="")

    class Meta(MaternalCrfModel.Meta):
        app_label = 'td_maternal'
        verbose_name = 'Substance Use Prior to Pregnancy'
        verbose_name_plural = 'Substance Use Prior to Pregnancy'