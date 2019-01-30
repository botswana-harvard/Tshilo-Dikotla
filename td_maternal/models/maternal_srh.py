from edc_constants.choices import YES_NO_DWTA

from django.db import models

from edc_base.model.fields import OtherCharField
from td_list.models import Contraceptives

from ..maternal_choices import REASON_UNSEEN_AT_CLINIC, REASON_CONTRACEPTIVE_NOT_INITIATED
from .maternal_crf_model import MaternalCrfModel


class MaternalSrh(MaternalCrfModel):

    """ A model completed by the user on the mother's use of sexual reproductive health services. """

    seen_at_clinic = models.CharField(
        verbose_name=('At the last visit, you had asked to be referred to the Sexual'
                      ' Reproductive Health Clinic.  Have you been seen in that clinic'
                      ' since your last visit with us?'),
        max_length=15,
        choices=YES_NO_DWTA)

    reason_unseen_clinic = models.CharField(
        verbose_name='If no, why not?',
        max_length=45,
        null=True,
        blank=True,
        choices=REASON_UNSEEN_AT_CLINIC)

    reason_unseen_clinic_other = OtherCharField(
        verbose_name='If Other, describe')

    is_contraceptive_initiated = models.CharField(
        verbose_name='If you did attend, did you initiate a contraceptive method?',
        max_length=15,
        choices=YES_NO_DWTA,
        null=True,
        blank=True,)

    contr = models.ManyToManyField(
        Contraceptives,
        blank=True,
        verbose_name='If yes, which method did you select? ',
        help_text='Tell us all that apply')

    contr_other = OtherCharField(
        max_length=35,
        verbose_name="If Other enter text description of other contraceptive method being used",
        blank=True,
        null=True)

    reason_not_initiated = models.CharField(
        verbose_name=('If you have not initiated a contraceptive method after attending'
                      ' a SRH clinic, please share with use the reason why you have not'
                      ' initiated a method'),
        max_length=45,
        choices=REASON_CONTRACEPTIVE_NOT_INITIATED,
        blank=True,
        null=True)

    reason_not_initiated_other = OtherCharField(
        verbose_name='If other is selected enter text',
        blank=True,
        null=True)

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Maternal SRH Services'
        verbose_name_plural = 'Maternal SRH Services'
