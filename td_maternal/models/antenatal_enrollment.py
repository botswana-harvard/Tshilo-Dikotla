from django.db import models

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords, UrlMixin
from edc_base.model.validators import date_not_future
from edc_consent.model_mixins import RequiresConsentMixin
from edc_constants.choices import YES_NO
from edc_export.model_mixins import ExportTrackingFieldsMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_protocol.validators import date_not_before_study_start
from edc_visit_schedule.model_mixins import EnrollmentModelMixin

from .antenatal_enrollment_mixin import AntenatalEnrollmentMixin


class AntenatalEnrollment(AntenatalEnrollmentMixin, EnrollmentModelMixin, OffstudyMixin, CreateAppointmentsMixin,
                          RequiresConsentMixin, ExportTrackingFieldsMixin, UrlMixin, BaseUuidModel):

    knows_lmp = models.CharField(
        verbose_name="Does the mother know the approximate date of the first day her last menstrual period?",
        choices=YES_NO,
        help_text='LMP',
        max_length=3)

    last_period_date = models.DateField(
        verbose_name="What is the approximate date of the first day of the mother's last menstrual period",
        validators=[
            date_not_before_study_start,
            date_not_future, ],
        null=True,
        blank=True,
        help_text='LMP')

    ga_lmp_enrollment_wks = models.IntegerField(
        verbose_name="GA by LMP at enrollment.",
        help_text=" (weeks of gestation at enrollment, LPM). Eligible if >16 and <36 weeks GA",
        null=True,
        blank=True,)

    ga_lmp_anc_wks = models.IntegerField(
        verbose_name="What is the mother's gestational age according to ANC records?",
        null=True,
        blank=True,
        help_text=" (weeks of gestation at enrollment, ANC)",)

    edd_by_lmp = models.DateField(
        verbose_name="Estimated date of delivery by lmp",
        validators=[
            date_not_before_study_start],
        null=True,
        blank=True,
        help_text="")

    history = HistoricalRecords()

    class Meta(EnrollmentModelMixin.Meta):
        app_label = 'td_maternal'
        verbose_name = 'Antenatal Enrollment'
        verbose_name_plural = 'Antenatal Enrollment'
        consent_model = 'td_maternal.maternalconsent'
        visit_schedule_name = 'maternal_visit_schedule.maternal_enrollment_step1'
