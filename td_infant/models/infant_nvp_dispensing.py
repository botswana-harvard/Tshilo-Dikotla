from django.db import models

from edc_constants.choices import YES_NO

from .infant_crf_model import InfantCrfModel


class InfantNvpDispensing(InfantCrfModel):

    nvp_prophylaxis = models.CharField(
        choices=YES_NO,
        max_length=3,
        help_text='',
        verbose_name='Was NVP infant prophylaxis administered to the infant after delivery?')

    reason_not_given = models.CharField(
        verbose_name='If NO, please give a reason why.',
        max_length=50,
        blank=True,
        null=True)

    azt_prophylaxis = models.CharField(
        choices=YES_NO,
        max_length=3,
        help_text='',
        verbose_name='Was AZT infant prophylaxis administered to the infant '
                     'after delivery in the hospital?')

    azt_dose_given = models.CharField(
        max_length=50,
        help_text='',
        blank=True,
        null=True,
        verbose_name='If YES, please specify how many doses of AZT were given.')

    nvp_admin_date = models.DateField(
        verbose_name="What date was NVP infant prophylaxis administered to infant?",
        blank=True,
        null=True)

    medication_instructions = models.CharField(
        verbose_name='Were instructions given to the mother on administration '
                     'of infant NVP prophylaxis?',
        choices=YES_NO,
        help_text='',
        max_length=3)

    dose_admin_infant = models.CharField(
        verbose_name='What was the dose of NVP infant prophylaxis administered to the infant? (in mL).',
        max_length=50,
        blank=True,
        null=True,
        help_text='Capture the actual dose the Government clinician gave at the initial dosing.')

    correct_dose = models.CharField(
        verbose_name='Was the NVP infant prophylaxis correct dose given?',
        choices=YES_NO,
        help_text='',
        max_length=3)

    corrected_dose = models.CharField(
        verbose_name='If NO, enter the corrected dose NVP infant prophylaxis administered'
                     'by the study clinician during the 72 hour delivery visit.',
        help_text='mL',
        blank=True,
        null=True,
        max_length=50)

    class Meta():
        app_label = 'td_infant'
        verbose_name = 'Infant Nevirapine Dispensing'
        verbose_name_plural = 'Infant Nevirapine Dispensing'
