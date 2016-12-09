from django.db import models

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.fields import OtherCharField
from edc_base.model.models import BaseUuidModel, HistoricalRecords, UrlMixin
from edc_consent.model_mixins import RequiresConsentMixin
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_pregnancy_utils.model_mixins import LabourAndDeliveryModelMixin
from edc_visit_schedule.model_mixins import EnrollmentModelMixin
from edc_visit_tracking.model_mixins import CrfInlineModelMixin

from td.choices import DX_MATERNAL
from td_list.models import DeliveryComplications

from ..managers import EnrollmentManager, MaternalLabDelDxTManager
from ..choices import DELIVERY_HEALTH_FACILITY, DELIVERY_MODE, CSECTION_REASON

from .maternal_crf_model import MaternalCrfModel


class MaternalLabDel(EnrollmentModelMixin, RequiresConsentMixin, LabourAndDeliveryModelMixin, CreateAppointmentsMixin,
                     UrlMixin, BaseUuidModel):

    """ A model completed by the user on Maternal Labor and Delivery which triggers registration of infants. """

    ADMIN_SITE_NAME = 'td_maternal_admin'

    delivery_hospital = models.CharField(
        verbose_name="Place of delivery? ",
        max_length=65,
        choices=DELIVERY_HEALTH_FACILITY,
        help_text="If 'OTHER', specify below")

    delivery_hospital_other = OtherCharField()

    labour_hrs = models.CharField(
        verbose_name="How long prior to to delivery, in HRS, did labour begin? ",
        max_length=10)

    mode_delivery = models.CharField(
        verbose_name="What was the mode of delivery?",
        max_length=100,
        choices=DELIVERY_MODE,
        help_text="If 'OTHER', specify below")

    mode_delivery_other = OtherCharField()

    csection_reason = models.CharField(
        verbose_name="If C-section was performed, indicate reason below",
        max_length=100,
        choices=CSECTION_REASON,
        help_text="If 'OTHER', specify below")

    csection_reason_other = OtherCharField()

    delivery_complications = models.ManyToManyField(
        DeliveryComplications,
        verbose_name="Were any of the following complications present at delivery? ",
        help_text="If 'OTHER', specify below")

    delivery_complications_other = OtherCharField()

    valid_regimen_duration = models.CharField(
        verbose_name="(Interviewer) If HIV+ve, has the participant been on the ART "
                     "regimen for at least 4 weeks in pregnancy?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        max_length=15,
        help_text=("If not 4 or more weeks then participant will go OFF STUDY."))

    arv_initiation_date = models.DateField(
        verbose_name="(Interviewer) If on ART, when did the participant initiate therapy for this pregnancy?",
        null=True,
        blank=True)

    delivery_comment = models.TextField(
        verbose_name="List any additional information about the labour and delivery (mother only) ",
        max_length=250,
        blank=True,
        null=True)

    comment = models.TextField(
        verbose_name="Comment if any additional pertinent information ",
        max_length=250,
        blank=True,
        null=True)

    objects = EnrollmentManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.live_infants_to_register = 1
        super(MaternalLabDel, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.subject_identifier)

    def natural_key(self):
        return (self.subject_identifier, )

    @property
    def subject_type(self):
        return'maternal'

    @property
    def study_site(self):
        return self.subject_identifier[4:6]

    class Meta(EnrollmentModelMixin.Meta):
        app_label = 'td_maternal'
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"
        consent_model = 'td_maternal.maternalconsent'
        visit_schedule_name = 'maternal_visit_schedule.follow_up'
        birth_model = 'td_infant.infantbirth'


class MaternalLabDelMed(MaternalCrfModel):

    """ Medical history collected during labor and delivery. """

    has_health_cond = models.CharField(
        verbose_name=(
            "Has the mother been newly diagnosed (during this pregnancy) "
            "with any major chronic health condition(s) that remain ongoing?"),
        max_length=3,
        choices=YES_NO)

#     health_cond = models.ManyToManyField(
#         HealthCond,
#         verbose_name="Select all that apply ")

    health_cond_other = OtherCharField()

    has_ob_comp = models.CharField(
        verbose_name=(
            "During this pregnancy, did the mother have any of the following "
            "obstetrical complications?"),
        max_length=3,
        choices=YES_NO)

#     ob_comp = models.ManyToManyField(
#         ObComp,
#         verbose_name="Select all that apply")

    ob_comp_other = OtherCharField()

    took_supplements = models.CharField(
        verbose_name="Did the mother take any of the following medications during this pregnancy?",
        max_length=3,
        choices=YES_NO)

#     supplements = models.ManyToManyField(
#         Supplements,
#         verbose_name="Please select relevant medications taken:",
#         help_text="Select all that apply")

    supplements_other = OtherCharField()

    comment = models.TextField(
        verbose_name="Comment if any additional pertinent information ",
        max_length=250,
        blank=True,
        null=True)

    history = HistoricalRecords()

    class Meta(MaternalCrfModel.Meta):
        app_label = 'td_maternal'
        verbose_name = "Delivery: Medical"
        verbose_name_plural = "Delivery: Medical"


class MaternalLabDelDx(MaternalCrfModel):

    """ Diagnosis during pregnancy collected during labor and delivery.
    This is for HIV positive mothers only"""

    has_who_dx = models.CharField(
        verbose_name=(
            "During this pregnancy, did the mother have any new diagnoses "
            "listed in the WHO Adult/Adolescent HIV clinical staging document which "
            "is/are NOT reported?"),
        max_length=3,
        choices=YES_NO_NA)

#     who = models.ManyToManyField(
#         WcsDxAdult,
#         verbose_name="List any new WHO Stage III/IV diagnoses that are not reported in Question 3 below:  ")

    has_preg_dx = models.CharField(
        verbose_name="During this pregnancy, did the mother have any of the following diagnoses? ",
        max_length=3,
        choices=YES_NO,
        help_text="If yes, Select all that apply in the table, only report grade 3 or 4 diagnoses")

    history = HistoricalRecords()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Delivery: Preg Dx"
        verbose_name_plural = "Delivery: Preg Dx"


class MaternalLabDelDxT (CrfInlineModelMixin, BaseUuidModel):

    """ Diagnosis during pregnancy collected during labor and delivery (transactions). """

    maternal_lab_del_dx = models.OneToOneField(MaternalLabDelDx)

    lab_del_dx = models.CharField(
        verbose_name="Diagnosis",
        max_length=175,
        choices=DX_MATERNAL)

    lab_del_dx_specify = models.CharField(
        verbose_name="Diagnosis specification",
        max_length=50,
        blank=True,
        null=True)

    grade = models.IntegerField(
        verbose_name="Grade")

    hospitalized = models.CharField(
        verbose_name="Hospitalized",
        max_length=3,
        choices=YES_NO)

    objects = MaternalLabDelDxTManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.lab_del_dx, ) + self.maternal_lab_del_dx.natural_key()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Delivery: Preg DxT"
        verbose_name_plural = "Delivery: Preg DxT"
