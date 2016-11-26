from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_visit_tracking.model_mixins import CrfInlineModelMixin

from td.choices import ARV_INTERRUPTION_REASON, ARV_DRUG_LIST, REASON_ARV_STOP

from ..managers import MaternalArvManager

from .maternal_crf_model import MaternalCrfModel


class MaternalArvPreg(MaternalCrfModel):

    """ This model is for all HIV positive mothers who are pregnant (whom we hope to enroll their infant)
     and/or for mothers who have just delivered """

    took_arv = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Did the mother receive any ARVs during this pregnancy?",
        help_text="(NOT including single -dose NVP in labour)")

    is_interrupt = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was there an interruption in the ARVs received during pregnancy through delivery of >/=3days?",
    )

    interrupt = models.CharField(
        verbose_name="Please give reason for interruption",
        max_length=50,
        choices=ARV_INTERRUPTION_REASON,
        default=NOT_APPLICABLE)

    interrupt_other = models.TextField(
        max_length=250,
        verbose_name="Other, specify ",
        blank=True,
        null=True)

    class Meta(MaternalCrfModel.Meta):
        app_label = 'td_maternal'
        verbose_name = 'Maternal ARV In This Preg'
        verbose_name_plural = 'Maternal ARV In This Preg'


class MaternalArv(CrfInlineModelMixin, BaseUuidModel):

    """ ARV table to indicate ARV medication taken by mother """

    maternal_arv_preg = models.ForeignKey(MaternalArvPreg)

    arv_code = models.CharField(
        verbose_name="ARV code",
        max_length=35,
        choices=ARV_DRUG_LIST,
        help_text='Regimen has to be at least 3.')

    start_date = models.DateField(
        verbose_name="Date Started",
        null=True,
        blank=False)

    stop_date = models.DateField(
        verbose_name="Date Stopped",
        null=True,
        blank=True)

    reason_for_stop = models.CharField(
        verbose_name="Reason for stop",
        choices=REASON_ARV_STOP,
        max_length=50,
        null=True,
        blank=True,
        help_text='If "Treatment Failure", notify study coordinator')

    reason_for_stop_other = models.CharField(
        max_length=100,
        verbose_name="Other, specify ",
        blank=True,
        null=True)

    objects = MaternalArvManager()

    def natural_key(self):
        return (self.arv_code, self.start_date) + self.maternal_arv_preg.natural_key()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Maternal ARV'
        verbose_name_plural = 'Maternal ARV'
        unique_together = ('maternal_arv_preg', 'arv_code')
