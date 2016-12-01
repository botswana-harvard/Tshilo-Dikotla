from django.db import models
from django.core.exceptions import ValidationError

from edc_base.model.models import BaseUuidModel, UrlMixin, HistoricalRecords
from edc_consent.model_mixins import RequiresConsentMixin
from edc_constants.constants import (FAILED_ELIGIBILITY)
from edc_metadata.model_mixins import CreatesMetadataModelMixin
from edc_visit_tracking.choices import VISIT_REASON
from edc_visit_tracking.model_mixins import (VisitModelMixin, CaretakerFieldsMixin)
from edc_visit_tracking.managers import VisitModelManager

from td.models import Appointment

from .antenatal_enrollment import AntenatalEnrollment


class MaternalVisitManager(VisitModelManager, models.Manager):

    def get_by_natural_key(self, subject_identifier, visit_code):
        return self.get(subject_identifier=subject_identifier, visit_code=visit_code)


class MaternalVisit(CreatesMetadataModelMixin, RequiresConsentMixin, CaretakerFieldsMixin,
                    VisitModelMixin, UrlMixin, BaseUuidModel):

    """ Maternal visit form that links all antenatal/ postnatal follow-up forms """

    appointment = models.OneToOneField(Appointment, on_delete=models.PROTECT)

    objects = MaternalVisitManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.subject_identifier, self.appointment.visit_code)

    def __str__(self):
        return '{} {} {}'.format(self.appointment.subject_identifier,
                                 self.appointment.visit_code)

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
            return AntenatalEnrollment.objects.get(
                subject_identifier=self.appointment.subject_identifier)
        except AntenatalEnrollment.DoesNotExist:
            return None

    def get_subject_identifier(self):
        return self.appointment.subject_identifier

    class Meta(VisitModelMixin.Meta):
        app_label = 'td_maternal'
        verbose_name = 'Maternal Visit'
        consent_model = 'td_maternal.maternalconsent'
        visit_schedule_name = 'maternal_visit_schedule'
