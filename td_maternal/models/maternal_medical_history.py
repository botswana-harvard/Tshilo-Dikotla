from django.db import models

# from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_code_lists.models import WcsDxAdult
from edc_constants.choices import YES_NO, YES_NO_NA

from td_list.models import ChronicConditions, MaternalMedications
from td_maternal.maternal_choices import KNOW_HIV_STATUS, LOWEST_CD4_KNOWN, IS_DATE_ESTIMATED

from .maternal_crf_model import MaternalCrfModel
from .maternal_consent import MaternalConsent


class MaternalMedicalHistory(MaternalCrfModel):

    """ A model completed by the user on Medical History for all mothers. """

    consent_model = MaternalConsent

    chronic_since = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name=("Does the mother have any significant chronic condition(s) that were"
                      " diagnosed prior to the current pregnancy and that remain ongoing?"),)

    who_diagnosis = models.CharField(
        max_length=25,
        choices=YES_NO_NA,
        verbose_name=("Prior to the current pregnancy, was the participant ever diagnosed with"
                      " a WHO Stage III or IV illness?"),
        help_text="Please use the WHO Staging Guidelines. ONLY for HIV infected mothers")

    who = models.ManyToManyField(
        WcsDxAdult,
        verbose_name="List any new WHO Stage III/IV diagnoses that are not reported")

    mother_chronic = models.ManyToManyField(
        ChronicConditions,
        related_name="mother",
        verbose_name="Does the mother have any of the above. Tick all that apply",
        help_text="")

    mother_chronic_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True)

    father_chronic = models.ManyToManyField(
        ChronicConditions,
        related_name="father",
        verbose_name="Does the father of the infant or the mother's other children have any of the above."
                     " Tick all that apply",
        help_text="")

    father_chronic_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True)

    mother_medications = models.ManyToManyField(
        MaternalMedications,
        verbose_name="Does the mother currently take any of the above medications."
                     " Tick all that apply",
        help_text="")

    mother_medications_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True)

    sero_posetive = models.CharField(
        max_length=25,
        verbose_name=("Is the mother HIV sero-positive?"),
        choices=YES_NO,)

    date_hiv_diagnosis = models.DateField(
        verbose_name="If HIV sero-posetive, what is the approximate date of diagnosis?",
        help_text='EDD Confirmed. Derived variable, see AntenatalEnrollment.',
        blank=True,
        null=True)

    perinataly_infected = models.CharField(
        max_length=25,
        verbose_name=("Was the mother peri-nataly infected with HIV?"),
        choices=YES_NO_NA,)

    know_hiv_status = models.CharField(
        max_length=50,
        verbose_name="How many people know that you are HIV infected?",
        choices=KNOW_HIV_STATUS)

    lowest_cd4_known = models.CharField(
        max_length=4,
        choices=LOWEST_CD4_KNOWN,
        verbose_name="Is the mother's lowest CD4 known?")

    cd4_count = models.IntegerField(
        verbose_name=("What was the mother's lowest known (nadir) CD4 cell count(cells/mm3)"
                      " at any time in the past?"),
        null=True,
        blank=True,
    )

    cd4_date = models.DateField(
        verbose_name="Year/Month of CD4 test ",
        help_text="Format is YYYY-MM-DD. Use 01 for Day",
        blank=True,
        null=True)

    is_date_estimated = models.CharField(
        max_length=50,
        choices=IS_DATE_ESTIMATED,
        verbose_name=("Is the subject's date of CD4 test estimated?"),
        blank=True,
        null=True
    )

    comment = models.TextField(
        max_length=250,
        verbose_name="Comments",
        blank=True,
        null=True)


    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Medical History"
        verbose_name_plural = "Maternal Medical History"
