from django.db import models

from edc_appointment.model_mixins import CreateAppointmentsOnEligibleMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords, UrlMixin
from edc_consent.model_mixins import RequiresConsentMixin
from edc_constants.choices import YES_NO
from edc_visit_schedule.model_mixins import EnrollmentModelMixin
from ..managers import EnrollmentManager

from ..managers import EnrollmentManager


class AntenatalEnrollmentTwo(EnrollmentModelMixin, RequiresConsentMixin, CreateAppointmentsOnEligibleMixin,
                             UrlMixin, BaseUuidModel):

    """An enrollment model for schedule maternal_enrollment_step2."""

    antenatal_visits = models.CharField(
        verbose_name='Are you ready to start the antenatal enrollment visits?',
        choices=YES_NO,
        help_text='',
        max_length=3)

    objects = EnrollmentManager()

    history = HistoricalRecords()

    def __str__(self):
        return self.subject_identifier

    def natural_key(self):
        return (self.subject_identifier, )

    class Meta(EnrollmentModelMixin.Meta):
        app_label = 'td_maternal'
        verbose_name = 'Antenatal Enrollment Two'
        verbose_name_plural = 'Antenatal Enrollment Two'
        consent_model = 'td_maternal.maternalconsent'
        visit_schedule_name = 'maternal_visit_schedule.maternal_enrollment_step2'
