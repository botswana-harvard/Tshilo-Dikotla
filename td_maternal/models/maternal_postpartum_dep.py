from django.db import models

from td.choices import LAUGH, ENJOYMENT, BLAME, UNHAPPY, ANXIOUS, SAD, PANICK, TOP, CRYING, HARM

from .maternal_crf_model import MaternalCrfModel


class MaternalPostPartumDep(MaternalCrfModel):

    laugh = models.CharField(
        max_length=75,
        verbose_name="In the past 7 days, I have been able to laugh and see the funny side of things?",
        choices=LAUGH,
        help_text="",
    )

    enjoyment = models.CharField(
        max_length=75,
        verbose_name="In the past 7 days, I looked forward with enjoyment of things?",
        choices=ENJOYMENT,
        help_text="",
    )

    blame = models.CharField(
        max_length=75,
        verbose_name="In the past 7 days, I have blamed myself unnecessarily when things went wrong",
        choices=BLAME,
        help_text="",
    )

    anxious = models.CharField(
        max_length=75,
        verbose_name="In the past 7 days, I have anxious or worried for no good reason",
        choices=ANXIOUS,
        help_text="",
    )

    panick = models.CharField(
        max_length=75,
        verbose_name="In the past 7 days, I have felt scared or panicky for no good reason",
        choices=PANICK,
        help_text="",
    )

    top = models.CharField(
        max_length=75,
        verbose_name="In the past 7 days, things have been getting on top of me",
        choices=TOP,
        help_text="",
    )

    unhappy = models.CharField(
        max_length=75,
        verbose_name="In the past 7 days, I have been so unhappy that I have had difficulty sleeping",
        choices=UNHAPPY,
        help_text="",
    )

    sad = models.CharField(
        max_length=75,
        verbose_name="In the past 7 days, I have felt sad or miserable",
        choices=SAD,
        help_text="",
    )

    crying = models.CharField(
        max_length=75,
        verbose_name="In the past 7 days, I have been so unhappy that I have been crying",
        choices=CRYING,
        help_text="",
    )

    self_harm = models.CharField(
        max_length=75,
        verbose_name="In the past 7 days, the thought of harming myself has occured to me",
        choices=HARM,
        help_text="",
    )

    class Meta(MaternalCrfModel.Meta):
        app_label = 'td_maternal'
        verbose_name = "Maternal Post Partum: Depression"
        verbose_name_plural = "Maternal Post Partum: Depression"
