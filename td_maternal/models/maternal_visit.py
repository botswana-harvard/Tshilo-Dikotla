from django.db import models
from django.core.exceptions import ValidationError
from django.apps import apps

from edc_base.model.models import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_constants.constants import (YES, POS, NEG, FAILED_ELIGIBILITY)
from edc_export.models import ExportTrackingFieldsMixin
from edc_offstudy.model_mixins import OffStudyMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_visit_tracking.choices import VISIT_REASON
from edc_visit_tracking.constants import COMPLETED_PROTOCOL_VISIT, LOST_VISIT
from edc_visit_tracking.model_mixins import (VisitModelMixin, PreviousVisitModelMixin, CaretakerFieldsMixin)
from edc_metadata.model_mixins import CreatesMetadataModelMixin

from td_appointment.models import Appointment
from td_registration.models import RegisteredSubject
from .maternal_consent import MaternalConsent
from .antenatal_enrollment import AntenatalEnrollment

from td_maternal.managers import MaternalVisitManager


class MaternalVisit(OffStudyMixin, SyncModelMixin, PreviousVisitModelMixin, CreatesMetadataModelMixin,
                    RequiresConsentMixin, CaretakerFieldsMixin, VisitModelMixin,
                    ExportTrackingFieldsMixin, BaseUuidModel):

    """ Maternal visit form that links all antenatal/ postnatal follow-up forms """

    appointment = models.OneToOneField(Appointment)

    off_study_model = ('td_maternal', 'MaternalOffStudy')

    death_report_model = ('td_maternal', 'MaternalDeathReport')

    history = SyncHistoricalRecords()

    objects = MaternalVisitManager()

    def natural_key(self):
        return (self.subject_identifier)

    def __str__(self):
        return '{} {} {}'.format(self.appointment.subject_identifier,
                                 self.antenatal_enrollment.registered_subject.first_name,
                                 self.appointment.visit_code)

    def is_off_study_on_previous_visit_or_raise(self):
        print(self.off_study_model._meta.get_fields(), "<><>><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><")
        #super().is_off_study_on_previous_visit_or_raises

    def save(self, *args, **kwargs):
        self.subject_identifier = self.appointment.subject_identifier
        if not self.is_eligible():
            self.reason = FAILED_ELIGIBILITY
        self.subject_failed_eligibility()
        super(MaternalVisit, self).save(*args, **kwargs)

    def get_visit_reason_choices(self):
        return VISIT_REASON

    def is_eligible(self):
        """Returns True if participant is either eligible antenataly."""
        eligible = False
        try:
            eligible = self.antenatal_enrollment.is_eligible or self.antenatal_enrollment.pending_ultrasound
        except AttributeError:
            pass
        return eligible

    def subject_failed_eligibility(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        if self.is_eligible() and self.reason == FAILED_ELIGIBILITY:
            raise exception_cls(
                "Subject is eligible. Visit reason cannot be 'Failed Eligibility'")

#     def get_visit_reason_no_follow_up_choices(self):
#         """ Returns the visit reasons that do not imply any data
#         collection; that is, the subject is not available. """
#         dct = {}
#         for item in VISIT_REASON_NO_FOLLOW_UP_CHOICES:
#             if item not in [COMPLETED_PROTOCOL_VISIT, LOST_VISIT]:
#                 dct.update({item: item})
#         return dct

#     @property
#     def scheduled_rapid_test(self):
#         """Returns the value of the \'result\' field of the RapidTestResult.
# 
#         This is a scheduled maternal form for on-study participants."""
#         RapidTestResult = apps.get_model('td_maternal', 'rapidtestresult')
#         try:
#             obj = RapidTestResult.objects.filter(
#                 maternal_visit__appointment__registered_subject=self.appointment.registered_subject,
#                 rapid_test_done=YES,
#                 result__in=[POS, NEG]).order_by('created').last()
#             scheduled_rapid_test = obj.result
#         except AttributeError as e:
#             if 'result' not in str(e):
#                 raise AttributeError(str(e))
#             scheduled_rapid_test = None
#         return scheduled_rapid_test

    @property
    def enrollment_hiv_status(self):
        enrollment_hiv_status = None
        try:
            enrollment_hiv_status = self.antenatal_enrollment.enrollment_hiv_status
        except AttributeError:
            pass
        return enrollment_hiv_status

    @property
    def antenatal_enrollment(self):
        try:
            registered_subject = RegisteredSubject.objects.get(
                subject_identifier=self.appointment.subject_identifier)
            return AntenatalEnrollment.objects.get(
                registered_subject=registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            return None

    def get_subject_identifier(self):
        return self.appointment.subject_identifier

#     @property
#     def postnatal_enrollment(self):
#         try:
#             return PostnatalEnrollment.objects.get(
#                 registered_subject=self.appointment.registered_subject)
#         except PostnatalEnrollment.DoesNotExist:
#             return None

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Maternal Visit'
        consent_model = 'td_maternal.maternalconsent'
