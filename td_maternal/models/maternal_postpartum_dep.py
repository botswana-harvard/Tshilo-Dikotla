from django.db import models
# from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_constants.choices import YES_NO, YES_NO_NA

from tshilo_dikotla.choices import LAUGH, ENJOYMENT, BLAME, UNHAPPY, ANXIOUS, SAD, PANICK, TOP, CRYING, HARM

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

    total_score = models.IntegerField(
        verbose_name="Total Depression score",
        default=0,
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.total_score = self.calculate_depression_score()
        super().save(*args, **kwargs)

    def calculate_depression_score(self):
        score = 0
        pos = {'laugh': LAUGH,
               'enjoyment': ENJOYMENT,
               'anxious': ANXIOUS}

        neg = {'blame': BLAME, 'panick': PANICK, 'top': TOP,
               'unhappy': UNHAPPY, 'sad': SAD,
               'crying': CRYING, 'self_harm': HARM}
        for f in self._meta.get_fields():
            if f.name in ['laugh', 'enjoyment', 'anxious']:
                choice_list = (getattr(self, f.name), getattr(self, f.name))
                score += pos.get(f.name).index(choice_list)
            elif f.name in ['blame', 'panick', 'top',
                            'unhappy', 'sad', 'crying', 'self_harm']:
                choice_list = (getattr(self, f.name), getattr(self, f.name))
                score += tuple(reversed(neg.get(f.name))).index(choice_list)
        return score

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Post Partum: Depression"
        verbose_name_plural = "Maternal Post Partum: Depression"
