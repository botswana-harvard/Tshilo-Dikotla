from django.db import models

# from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_constants.constants import NOT_APPLICABLE
from edc_constants.choices import (NORMAL_ABNORMAL, YES_NO_UNKNOWN,
                                   YES_NO_NOT_EVALUATED_NA, NORMAL_ABNORMAL_NOEXAM)

from tshilo_dikotla.apps.td_list.models import Foods, Rations

from .infant_crf_model import InfantCrfModel


class SolidFoodAssessment(InfantCrfModel):

    """ A model completed by the user on the infant's solid food assessment. """

    age_solid_food = models.IntegerField(
        verbose_name="At approximately what age, in months did this child start receiving solid foods"
                     " (foods other than breast milk or formula?)",
        help_text="Months.",
    )

    solid_foods = models.ManyToManyField(
        Foods,
        max_length=15,
        verbose_name="For infants and children who are taking solid foods, what foods is your infant/child taking"
                     " (choose all that apply.)",
        help_text=""
    )

    solid_foods_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    porridge = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had any porridge?",
        help_text="")

    porridge_freq = models.IntegerField(
        verbose_name="If yes, please indicate how many times this child has had porridge in the last week",
        help_text="",
        blank=True,
        null=True,
    )

    tsabana = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had any tsabana?",
        help_text="")

    tsabana_week = models.IntegerField(
        verbose_name="If yes, then please indicate how many times this child usually eats tsabana in a week",
        help_text="",
        blank=True,
        null=True,
    )

    mother_tsabana = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Does the mother in this child's household usually eat tsabana?",
        help_text="")

    meat = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had any meat, chicken or fish?",
        help_text="")

    meat_freq = models.IntegerField(
        verbose_name="If yes, please indicate how many times this child has had meat, chicken or fish in the last week",
        help_text="",
        blank=True,
        null=True,
    )

    potatoes = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had any potatoes?",
        help_text=" Do not count a sweet potato under this question.")

    potatoes_freq = models.IntegerField(
        verbose_name="If yes, please indicate how many times this child has had meat, chicken or fish in the last week",
        help_text="",
        blank=True,
        null=True,
    )

    carrot_swt_potato = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had pumpkin, carrot or sweet potato?",
        help_text="")

    carrot_swt_potato_freq = models.IntegerField(
        verbose_name="If yes, please indicate how many times this child has had carrot, pumpkin or sweet potato"
                     " in the last week",
        help_text="",
        blank=True,
        null=True,
    )

    green_veg = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had any green vegetables?",
        help_text="")

    green_veg_freq = models.IntegerField(
        verbose_name="If yes, please indicate how many times this child has had green vegetables in the last week",
        help_text="",
        blank=True,
        null=True,
    )

    fresh_fruits = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had any fresh fruits?",
        help_text="")

    fresh_fruits_freq = models.IntegerField(
        verbose_name="If yes, please indicate how many times this child has had fresh fruits in the last week",
        help_text="",
        blank=True,
        null=True,
    )

    fullcream_milk = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had any full cream milk?",
        help_text="Powdered, fresh or long-life")

    fullcream_milk_freq = models.IntegerField(
        verbose_name="If yes, please indicate how many times this child has had full cream milk in the last week",
        help_text="",
        blank=True,
        null=True,
    )
    skim_milk = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had any skim or part-skim milk?",
        help_text="Powdered, fresh or long-life")

    skim_milk_freq = models.IntegerField(
        verbose_name="If yes, please indicate how many times this child has had any skim or part-skim in the last week",
        help_text="",
        blank=True,
        null=True,
    )

    raw_milk = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had any raw animal milk?",
        help_text="")

    raw_milk_freq = models.IntegerField(
        verbose_name="If yes, please indicate how many times this child has had raw animal milk in the last week",
        help_text="",
        blank=True,
        null=True,
    )

    juice = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had any juice?",
        help_text="")

    juice_freq = models.IntegerField(
        verbose_name="If yes, please indicate how many times this child has had juice in the last week",
        help_text="",
        blank=True,
        null=True,
    )

    eggs = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had any eggs?",
        help_text="")

    eggs_freq = models.IntegerField(
        verbose_name="If yes, please indicate how many times this child has had eggs in the last week",
        help_text="",
        blank=True,
        null=True,
    )

    yogurt = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had any yogurt?",
        help_text="")

    yogurt_freq = models.IntegerField(
        verbose_name="If yes, please indicate how many times this child has had yogurt in the last week",
        help_text="",
        blank=True,
        null=True,
    )

    cheese = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Since this time yesterday, has this child had any cheese?",
        help_text="")

    cheese_freq = models.IntegerField(
        verbose_name="If yes, please indicate how many times this child has had cheese in the last week",
        help_text="",
        blank=True,
        null=True,
    )

    rations = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="At this child's last visit to this clinic for growth evaluation, did this child receive any"
                     " ration?",
        help_text="")

    rations_receviced = models.ManyToManyField(
        Rations,
        verbose_name="If yes, please indicate all applicable rations received at the last visit",
        help_text="",
    )

#     history = AuditTrail()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Solid Food Assessment"
        verbose_name_plural = "Infant Solid Food Assessment"
