from django.db import models, transaction
# from django.db.models import get_model

from edc_appointment.models import AppointmentMixin
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future,)
from edc_consent.models import RequiresConsentMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import NO, YES
from edc_export.models import ExportTrackingFieldsMixin
from edc_offstudy.models import OffStudyMixin
from edc_sync.models import SyncModelMixin

# from ..managers import PostnatalEnrollmentManager
from ..maternal_choices import LIVE_STILL_BIRTH

# from .enrollment_helper import EnrollmentError
# from .enrollment_mixin import EnrollmentMixin
from .maternal_consent import MaternalConsent
from tshilo_dikotla.apps.td.constants import STILL_BIRTH


class PostnatalEnrollment(SyncModelMixin, OffStudyMixin, AppointmentMixin,
                          RequiresConsentMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    consent_model = MaternalConsent

    off_study_model = ('td_maternal', 'MaternalOffStudy')

    weeks_base_field = 'gestation_wks_delivered'  # for rapid test required calc

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    postpartum_days = models.IntegerField(
        verbose_name="How many days postpartum?",
        null=True,
        help_text="If more than 3days, not eligible")

    vaginal_delivery = models.CharField(
        verbose_name="Was this a vaginal delivery?",
        choices=YES_NO,
        max_length=3,
        help_text="INELIGIBLE if NO")

    gestation_wks_delivered = models.IntegerField(
        verbose_name="What was the gestational age of the newborn at birth?",
        help_text="ineligible if premature or born before 37weeks")

    delivery_status = models.CharField(
        verbose_name="Was this a live or still birth?",
        choices=LIVE_STILL_BIRTH,
        max_length=15,
        help_text='if still birth, not eligible')

    live_infants = models.IntegerField(
        verbose_name="How many live infants?",
        null=True,
        blank=True)

#     objects = PostnatalEnrollmentManager()

    history = AuditTrail()

    def natural_key(self):
        return (self.report_datetime, self.registered_subject.natural_key())

    def save(self, *args, **kwargs):
        self.update_with_common_fields_from_antenatal_enrollment()
        self.is_eligible_if_antenatal_exists_or_raise()
        super(PostnatalEnrollment, self).save(*args, **kwargs)

    def unenrolled_error_messages(self):
        """Returns a tuple (True, None) if mother is eligible otherwise
        (False, unenrolled_error_message) where error message is the reason enrollment failed."""
        unenrolled_error_message = []
        chronic_message = self.chronic_and_postpartum_unenrolled_error_messages()
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
        return (self.is_eligible, ', '.join(unenrolled_error_message))

    def chronic_and_postpartum_unenrolled_error_messages(self):
        unenrolled_error_message = None
        if self.is_diabetic == YES:
            unenrolled_error_message = 'Diabetic'
        if self.on_tb_tx == YES:
            unenrolled_error_message = 'on TB treatment'
        if self.on_hypertension_tx == YES:
            unenrolled_error_message = 'Hypertensive'
        # postpartum
        if self.postpartum_days > 3:
            unenrolled_error_message = 'postpartum > 3days'
        if self.vaginal_delivery == NO:
            unenrolled_error_message = 'not vaginal delivery'
        if self.gestation_wks_delivered < 37:
            unenrolled_error_message = 'born before 37wks'
        if self.delivery_status == STILL_BIRTH:
            unenrolled_error_message = 'still birth'
        return unenrolled_error_message

    def get_registration_datetime(self):
        return self.report_datetime

#     def is_eligible_if_antenatal_exists_or_raise(self, exception_cls=None):
#         exception_cls = exception_cls or EnrollmentError
#         AntenatalEnrollment = get_model('mb_maternal', 'antenatalenrollment')
#         with transaction.atomic():
#             try:
#                 antenatal_enrollment = AntenatalEnrollment.objects.get(
#                     registered_subject=self.registered_subject)
#                 if not antenatal_enrollment.is_eligible:
#                     raise EnrollmentError(
#                         'Subject was determined ineligible at Antenatal '
#                         'Enrollment on {}. Cannot continue.'.format(
#                             antenatal_enrollment.report_datetime))
#             except AntenatalEnrollment.DoesNotExist:
#                 pass

#     @property
#     def off_study_visit_code(self):
#         """Returns the visit code for the off-study visit if eligibility criteria fail.
# 
#         Returns either 1000M or, if Antenatal Enrollment exists, 2000M."""
#         try:
#             AntenatalEnrollment = get_model('mb_maternal', 'antenatalenrollment')
#             AntenatalEnrollment.objects.get(registered_subject=self.registered_subject)
#             off_study_visit_code = '2000M'
#         except AntenatalEnrollment.DoesNotExist:
#             off_study_visit_code = '1000M'
#         return off_study_visit_code

#     def update_with_common_fields_from_antenatal_enrollment(self):
#         """Updates common field values from Antenatal Enrollment to
#         this instance if not already set.
# 
#         Only updates if AntenatalEnrollment.is_eligible=True."""
#         AntenatalEnrollment = get_model('mb_maternal', 'antenatalenrollment')
#         try:
#             antenatal_enrollment = AntenatalEnrollment.objects.get(
#                 registered_subject=self.registered_subject,
#                 is_eligible=True)
#             for attrname in self.common_fields():
#                 if not getattr(self, attrname):
#                     setattr(self, attrname, getattr(antenatal_enrollment, attrname))
#         except AntenatalEnrollment.DoesNotExist:
#             pass

#     @property
#     def antenatal_enrollment(self):
#         """Is this ever used??"""
#         AntenatalEnrollment = get_model('mb_maternal', 'antenatalenrollment')
#         try:
#             return AntenatalEnrollment.objects.get(registered_subject=self.registered_subject)
#         except AntenatalEnrollment.DoesNotExist:
#             return None
#         return None

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Postnatal Enrollment'
        verbose_name_plural = 'Postnatal Enrollment'
