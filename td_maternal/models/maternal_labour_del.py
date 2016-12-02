from django.db import models

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.fields import OtherCharField
from edc_base.model.models import BaseUuidModel, HistoricalRecords, UrlMixin
from edc_base.model.validators import datetime_not_future
from edc_consent.model_mixins import RequiresConsentMixin
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_protocol.validators import datetime_not_before_study_start
from edc_registration.model_mixins import SubjectIdentifierFromRegisteredSubjectModelMixin
from edc_visit_tracking.model_mixins import CrfInlineModelMixin

from td.choices import DX_MATERNAL
from td_list.models import DeliveryComplications

from ..managers import EnrollmentManager, MaternalLabDelDxTManager
from ..maternal_choices import DELIVERY_HEALTH_FACILITY, DELIVERY_MODE, CSECTION_REASON

from .maternal_crf_model import MaternalCrfModel


class MaternalLabourDel(SubjectIdentifierFromRegisteredSubjectModelMixin, CreateAppointmentsMixin,
                        RequiresConsentMixin, UrlMixin, BaseUuidModel):

    """ A model completed by the user on Maternal Labor and Delivery which triggers registration of infants. """

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    delivery_datetime = models.DateTimeField(
        verbose_name="Date and time of delivery :",
        help_text="If TIME unknown, estimate",
        validators=[
            datetime_not_future, ])

    delivery_time_estimated = models.CharField(
        verbose_name="Is the delivery TIME estimated?",
        max_length=3,
        choices=YES_NO)

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

    live_infants_to_register = models.IntegerField(
        verbose_name="How many babies are you registering to the study? ")

    valid_regiment_duration = models.CharField(
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
        super(MaternalLabourDel, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.subject_identifier)

    def natural_key(self):
        return (self.subject_identifier, )

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"
        consent_model = 'td_maternal.maternalconsent'
        visit_schedule_name = 'maternal_visit_schedule'


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


class MaternalHivInterimHx(MaternalCrfModel):

    """ Laboratory and other clinical information collected during labor and delivery.
    for HIV +ve mothers ONLY"""

    has_cd4 = models.CharField(
        verbose_name=("During this pregnancy did the mother have at least one CD4 count"
                      " performed (outside the study)? "),
        max_length=3,
        choices=YES_NO)

    cd4_date = models.DateField(
        verbose_name="Date of most recent CD4 test? ",
        blank=True,
        null=True)

    cd4_result = models.CharField(
        verbose_name="Result of most recent CD4 test",
        max_length=35,
        blank=True,
        null=True)

    has_vl = models.CharField(
        verbose_name=("During this pregnancy did the mother have a viral load perfomed"
                      " (outside the study)? "),
        max_length=3,
        choices=YES_NO,
        help_text="(if 'YES' continue. Otherwise go to question 9)")

    vl_date = models.DateField(
        verbose_name="If yes, Date of most recent VL test? ",
        blank=True,
        null=True)

    vl_detectable = models.CharField(
        verbose_name="Was the viral load detectable?",
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="")

    vl_result = models.CharField(
        verbose_name="Result of most recent VL test",
        max_length=35,
        blank=True,
        null=True)

    comment = models.TextField(
        verbose_name="Comment if any additional pertinent information ",
        max_length=250,
        blank=True,
        null=True)

    history = HistoricalRecords()

    class Meta(MaternalCrfModel.Meta):
        app_label = 'td_maternal'
        verbose_name = "Maternal Hiv Interim Hx"
        verbose_name_plural = "Maternal Hiv Interim Hx"
#         verbose_name = "Delivery: Clinical"
#         verbose_name_plural = "Delivery: Clinical"


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
