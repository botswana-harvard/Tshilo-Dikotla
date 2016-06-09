from dateutil.relativedelta import relativedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.apps import apps

from edc_appointment.models import AppointmentMixin
# from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future, 
    date_not_before_study_start, date_not_future)
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

    weeks_base_field = 'ga_lmp_enrollment_wks'

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    last_period_date = models.DateField(
        verbose_name="What is the approximate date of the first day of the mother’s last menstrual period",
        validators=[
            date_not_before_study_start,
            date_not_future, ],
        help_text='LMP')

    ga_lmp_enrollment_wks = models.IntegerField(
        verbose_name="GA by LMP at enrollment.",
        help_text=" (weeks of gestation at enrollment, LPM). Eligible if >16 and <36 weeks GA",)

    ga_lmp_anc_wks = models.IntegerField(
        verbose_name="What is the mother's gestational age according to ANC records?",
        null=True,
        blank=True,
        help_text=" (weeks of gestation at enrollment, ANC)",)

    edd_by_lmp = models.DateField(
        verbose_name="Estimated date of delivery by lmp",
        validators=[
            date_not_before_study_start],
        help_text="")


#     objects = AntenatalEnrollmentManager()
    objects = models.Manager()

#     history = AuditTrail()

    def save(self, *args, **kwargs):
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
        if self.will_get_arvs == NO:
            unenrolled_error_message.append('Will not get ARVs on this pregnancy.')
        if self.rapid_test_done == NO:
            unenrolled_error_message.append('rapid test not done')
        if self.ga_lmp_enrollment_wks < 16 or self.ga_lmp_enrollment_wks > 36:
            unenrolled_error_message.append('gestation not 16 to 36wks')
        return unenrolled_error_message

    def chronic_unenrolled_error_messages(self):
        unenrolled_error_message = None
        if self.is_diabetic == YES:
            unenrolled_error_message = 'Diabetic'
        return unenrolled_error_message

    @property
    def off_study_visit_code(self):
        """Returns the visit code for the off-study visit if eligibility criteria fail."""
        return '1000M'

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Antenatal Enrollment'
        verbose_name_plural = 'Antenatal Enrollment'
