from django.db import models

# from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_constants.choices import ARV_STATUS_WITH_NEVER
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE
# from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models.crf_inline_model_mixin import CrfInlineModelMixin

from ..managers import MaternalArvPostModManager
from ..maternal_choices import REASON_FOR_HAART, ARV_DRUG_LIST, DOSE_STATUS, ARV_MODIFICATION_REASON

from .maternal_crf_model import MaternalCrfModel


class MaternalArvPost (MaternalCrfModel):

    """ A model completed by the user on the mother's ARVs administered post-partum. """

    on_arv_since = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name=("Was the mother supposed to be on triple ARVs any time since the last"
                      " attended scheduled visit?"),
        help_text="If 'NO' End. Otherwise continue go to section one",)

    on_arv_reason = models.CharField(
        verbose_name="Reason for triple ARVs ",
        max_length=25,
        choices=REASON_FOR_HAART,
        default=NOT_APPLICABLE,
        help_text="",)

    on_arv_reason_other = models.TextField(
        max_length=35,
        verbose_name="if other, specify",
        blank=True,
        null=True,)

    arv_status = models.CharField(
        verbose_name=("What is the status of the participant's antiretroviral"
                      " treatment / prophylaxis at this visit or since the last visit? "),
        max_length=25,
        choices=ARV_STATUS_WITH_NEVER,
        default=NOT_APPLICABLE,)

    def visit(self):
        return self.maternal_visit

    def __str__(self):
        return str(self.maternal_visit)

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal ARV Post"
        verbose_name_plural = "Maternal ARV Post"


class MaternalArvPostMed(CrfInlineModelMixin, BaseUuidModel):

    """ Maternal ARV modifications post-partum.

    if art_status never, no_mod or N/A then this is not required"""

    maternal_arv_post = models.ForeignKey(MaternalArvPost)

    arv_code = models.CharField(
        verbose_name="ARV Code",
        max_length=25,
        choices=ARV_DRUG_LIST)

    dose_status = models.CharField(
        max_length=25,
        choices=DOSE_STATUS,
        verbose_name="Dose Status")

    modification_date = models.DateField(
        verbose_name="Date ARV Modified")

    modification_code = models.CharField(
        max_length=50,
        choices=ARV_MODIFICATION_REASON,
        verbose_name="Reason for Modification")

    objects = MaternalArvPostModManager()

    def natural_key(self):
        return (self.arv_code, self.modification_date) + self.maternal_arv_post.natural_key()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Maternal ARVs Post: Meds'
        verbose_name_plural = 'Maternal ARVs Post: Meds'
        unique_together = ('maternal_arv_post', 'arv_code', 'modification_date')


class MaternalArvPostAdh(MaternalCrfModel):

    """Maternal ARV adherence post-partum"""

    missed_doses = models.IntegerField(
        verbose_name=("Since the last attended last scheduled visit, how many doses of"
                      " triple ARVs were missed? "))

    missed_days = models.IntegerField(
        verbose_name=("Since the last attended scheduled visit, how many entire days"
                      " were triple ARVS not taken?"),
        default=0)

    missed_days_discnt = models.IntegerField(
        verbose_name=("If triple ARVs discontinued by health provider, how many days were triple ARVs missed"
                      " prior to discontinuation?"),
        default=0)

    comment = models.TextField(
        max_length=250,
        verbose_name="Comment",
        blank=True,
        null=True)
    
    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal ARVs Post: Adherence"
        verbose_name_plural = "Maternal ARVs Post: Adherence"
