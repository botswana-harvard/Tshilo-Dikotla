from django.db import models

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords, UrlMixin
from edc_base.model.validators import datetime_not_future
from edc_consent.model_mixins import RequiresConsentMixin
from edc_constants.choices import YES_NO
from edc_protocol.validators import datetime_not_before_study_start
from edc_visit_schedule.model_mixins import EnrollmentModelMixin


class Manager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class AntenatalEnrollmentTwo(EnrollmentModelMixin, RequiresConsentMixin, CreateAppointmentsMixin,
                             UrlMixin, BaseUuidModel):

    """An enrollment model for schedule maternal_enrollment_step2."""

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    antenatal_visits = models.CharField(
        verbose_name='Are you ready to start the antenatal enrollment visits?',
        choices=YES_NO,
        help_text='',
        max_length=3)

    objects = Manager()

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
        visit_schedule_name = 'maternal_visit_schedule'
