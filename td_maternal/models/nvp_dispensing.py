from django.db import models

from edc_constants.choices import YES_NO

from .maternal_lab_del import MaternalLabDel
from .maternal_crf_model import MaternalCrfModel


class NvpDispensing(MaternalCrfModel):

    maternal_delivery = models.ForeignKey(
        MaternalLabDel,
        verbose_name='Delivery Record')

    nvp_admin_date = models.DateField(
        verbose_name="Date NVP was administered to infant.",)

    medication_instructions = models.CharField(
        verbose_name='Were instructions given to the mother on administration of the medication?',
        choices=YES_NO,
        help_text='',
        max_length=3)

    dose_admin_infant = models.CharField(
        verbose_name='Dose administered to infant.',
        max_length=50,
        help_text='Capture the actual dose the Government clinician gave at the initial dosing.')

    correct_dose = models.CharField(
        verbose_name='Was the correct dose given?',
        choices=YES_NO,
        help_text='',
        max_length=3)

    corrected_dose = models.CharField(
        verbose_name='If NO, please enter corrected dose.',
        help_text='Capture the corrected dose made by the study clinician during the 72-hour post delivery visit',
        blank=True,
        null=True,
        max_length=50)

    dose_adjustment = models.CharField(
        verbose_name='Has the infant come for week 2 dose adjustment?',
        choices=YES_NO,
        help_text='',
        max_length=3)

    week_2_dose = models.CharField(
        verbose_name='IF YES, please enter the week 2 dose',
        help_text='Capture the week 2 dose adjustment due to weight.',
        blank=True,
        null=True,
        max_length=50)

    class Meta(MaternalCrfModel.Meta):
        app_label = 'td_maternal'
        verbose_name = 'Nevirapine Dispensing'
        verbose_name_plural = 'Nevirapine Dispensing'
