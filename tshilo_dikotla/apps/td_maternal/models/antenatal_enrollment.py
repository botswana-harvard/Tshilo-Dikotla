from django.db import models

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

    weeks_base_field = 'gestation_wks'  # for rapid test required calc

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    last_period_date = models.DateTimeField(
        verbose_name="What is the approximate date of the first day of the mother’s last menstrual period",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    gestation_wks = models.IntegerField(
        verbose_name="How many weeks pregnant is the mother by LMP?",
        help_text=" (weeks of gestation). Eligible if >16 and <36 weeks GA", )

#     objects = AntenatalEnrollmentManager()
    objects = models.Manager()

#     history = AuditTrail()

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
        if self.gestation_wks < 16 or self.gestation_wks > 36:
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

#     def update_common_fields_to_postnatal_enrollment(self):
#         """Updates common field values from Antenatal Enrollment to
#         Postnatal Enrollment if Postnatal Enrollment exists.
# 
#         Confirms is_eligible does not change value before saving."""
#         if self.id and self.is_eligible:
#             try:
#                 postnatal_enrollment = PostnatalEnrollment.objects.get(
#                     registered_subject=self.registered_subject)
#                 for attrname in self.common_fields():
#                     setattr(postnatal_enrollment, attrname, getattr(self, attrname))
#                 is_eligible = EnrollmentHelper(postnatal_enrollment).is_eligible
#                 if is_eligible != postnatal_enrollment.is_eligible:
#                     raise EnrollmentError(
#                         'Eligiblity calculated for Postnatal Enrollment unexpectedly '
#                         'changed after updating values from Antenatal Enrollment. '
#                         'Got \'is_eligible\' changed from {} to {}.'.format(
#                             is_eligible, postnatal_enrollment.is_eligible))
#                 else:
#                     postnatal_enrollment.save()
#             except PostnatalEnrollment.DoesNotExist:
#                 pass

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Antenatal Enrollment'
        verbose_name_plural = 'Antenatal Enrollment'
