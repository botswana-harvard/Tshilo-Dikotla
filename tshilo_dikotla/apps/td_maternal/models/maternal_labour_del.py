from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
# from edc_code_lists.models import WcsDxAdult
from edc_constants.choices import YES_NO, YES_NO_UNKNOWN, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfInlineModelMixin
from edc_registration.models import RegisteredSubject
from edc_consent.models import RequiresConsentMixin
from edc_appointment.models import AppointmentMixin

from tshilo_dikotla.apps.td.choices import DX_MATERNAL
# from tshilo_dikotla.apps.td_list.models import Supplements, HealthCond, ObComp

# from ..managers import MaternalLabDelDxTManager
from ..maternal_choices import DELIVERY_HEALTH_FACILITY

from .maternal_consent import MaternalConsent
from .maternal_crf_model import MaternalCrfModel


class MaternalLabourDel(RequiresConsentMixin, AppointmentMixin, BaseUuidModel):

    """ A model completed by the user on Maternal Labor and Delivery which triggers registration of infants. """

    consent_model = MaternalConsent

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

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

    labour_hrs = models.CharField(
        verbose_name="How long prior to to delivery, in HRS, did labour begin? ",
        max_length=10)

    delivery_hospital = models.CharField(
        verbose_name="Where did the participant deliver? ",
        max_length=65,
        choices=DELIVERY_HEALTH_FACILITY,
        help_text="If 'OTHER', specify below")

    delivery_hospital_other = OtherCharField()

    has_uterine_tender = models.CharField(
        verbose_name="Was uterine tenderness recorded? ",
        max_length=10,
        choices=YES_NO_UNKNOWN)

    has_temp = models.CharField(
        verbose_name="Is the maximum temparature known?",
        max_length=3,
        choices=YES_NO)

    labour_max_temp = models.DecimalField(
        verbose_name="Indicate the maximum temperature of mother during labour",
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(36.5), MaxValueValidator(39.0), ],
        blank=True,
        null=True)

    has_chorioamnionitis = models.CharField(
        verbose_name="Was chorio-amnionitis suspected? ",
        max_length=3,
        choices=YES_NO)

    delivery_complications = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Were there other complications at delivery? ")

    live_infants_to_register = models.IntegerField(
        verbose_name="How many babies are you registering to the study? ")

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

#     history = AuditTrail()
    objects = models.Manager()

    def get_registration_datetime(self):
        return self.report_datetime

    @property
    def subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"


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

    history = AuditTrail()

    class Meta:
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

    history = AuditTrail()

    class Meta:
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

    history = AuditTrail()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Delivery: Preg Dx"
        verbose_name_plural = "Delivery: Preg Dx"


class MaternalLabDelDxT (CrfInlineModelMixin, SyncModelMixin, BaseUuidModel):

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

#     objects = MaternalLabDelDxTManager()

    history = AuditTrail()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Delivery: Preg DxT"
        verbose_name_plural = "Delivery: Preg DxT"
