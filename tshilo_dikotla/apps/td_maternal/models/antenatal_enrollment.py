from dateutil.relativedelta import relativedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.apps import apps

from edc_base.model.validators import date_not_before_study_start
from edc_appointment.models import AppointmentMixin
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future,)
from edc_export.models import ExportTrackingFieldsMixin
from edc_consent.models import RequiresConsentMixin
from edc_constants.constants import NO, YES
from edc_offstudy.models import OffStudyMixin
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin

#from ..managers import AntenatalEnrollmentManager

from .enrollment_mixin import EnrollmentMixin
from .maternal_consent import MaternalConsent
# from .postnatal_enrollment import PostnatalEnrollment


class AntenatalEnrollment(EnrollmentMixin, OffStudyMixin, AppointmentMixin,
                          RequiresConsentMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    consent_model = MaternalConsent

    off_study_model = ('td_maternal', 'MaternalOffStudy')

    weeks_base_field = 'gestation_wks_lmp_lmp'  # for rapid test required calc

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    last_period_date = models.DateField(
        verbose_name="What is the approximate date of the first day of the mother’s last menstrual period",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='LMP')

    gestation_wks_lmp = models.IntegerField(
        verbose_name="How many weeks pregnant is the mother by LMP?",
        help_text=" (weeks of gestation). Eligible if >16 and <36 weeks GA", )

    edd_by_lmp = models.DateField(
        verbose_name="Estimated date of delivery by lmp",
        validators=[
            date_not_before_study_start],
        help_text="EDD by LMP using Naegele's rule")


#     objects = AntenatalEnrollmentManager()    
    objects = models.Manager()

#     history = AuditTrail()

    def save(self, *args, **kwargs):
        # TODO: validate that values in Antenatal Enrollment that are used in MartenalUltrasound have not been changed,
        # if an instance of maternal ultrasound exists.
        self.edd_by_lmp = self.evaluate_edd_by_lmp()
        super(AntenatalEnrollment, self).save(*args, **kwargs)

    def natural_key(self):
        return self.registered_subject.natural_key()
    natural_key.dependencies = ['edc_registration.registeredsubject']

    def unenrolled_error_messages(self):
        """Returns a tuple (True, None) if mother is eligible otherwise
        (False, unenrolled_error_message) where error message is the reason enrollment failed."""
        unenrolled_error_message = []
        chronic_message = self.chronic_unenrolled_error_messages()
        unenrolled_error_message.append(chronic_message) if chronic_message else None
        if self.will_breastfeed == NO:
            unenrolled_error_message.append('will not breastfeed')
        if self.will_remain_onstudy == NO:
            unenrolled_error_message.append('won\'t remain in study')
        if self.week32_test == NO:
            unenrolled_error_message.append('no week32 test')
        if self.evidence_hiv_status == NO:
            unenrolled_error_message.append('no HIV status evidence')
        if self.valid_regimen == NO:
            unenrolled_error_message.append('not on valid regimen')
        if self.valid_regimen_duration == NO:
            unenrolled_error_message.append('regimen duration invalid')
        if self.rapid_test_done == NO:
            unenrolled_error_message.append('rapid test not done')
        if self.gestation_wks_lmp < 16 or self.gestation_wks_lmp > 36:
            unenrolled_error_message.append('gestation not 16 to 36wks')
        return (self.is_eligible, ', '.join(unenrolled_error_message))

    def chronic_unenrolled_error_messages(self):
        unenrolled_error_message = None
        if self.is_diabetic == YES:
            unenrolled_error_message = 'Diabetic'
        return unenrolled_error_message

    @property
    def off_study_visit_code(self):
        """Returns the visit code for the off-study visit if eligibility criteria fail."""
        return '1000M'

    def evaluate_edd_by_lmp(self):
        # Using Naegele's rule
        return (self.last_period_date + relativedelta(years=1) + relativedelta(days=7)) - relativedelta(months=3)

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Antenatal Enrollment'
        verbose_name_plural = 'Antenatal Enrollment'
