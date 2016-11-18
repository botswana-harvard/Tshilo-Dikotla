from django.db import models

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_future, date_not_future
from edc_consent.model_mixins import RequiresConsentMixin
from edc_constants.choices import YES_NO
from edc_export.model_mixins import ExportTrackingFieldsMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_base.model.models import HistoricalRecords
from td_registration.models import RegisteredSubject

from ..managers import AntenatalVisitMembershipManager

from .maternal_consent import MaternalConsent
from edc_base.model.models.url_mixin import UrlMixin


class AntenatalVisitMembership(RequiresConsentMixin, CreateAppointmentsMixin, UrlMixin, BaseUuidModel):

    consent_model = MaternalConsent

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

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

    objects = AntenatalVisitMembershipManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        super(AntenatalVisitMembership, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.registered_subject.subject_identifier)

    def natural_key(self):
        return self.registered_subject.natural_key()
    natural_key.dependencies = ['edc_registration.registeredsubject']

    def get_registration_datetime(self):
        return self.report_datetime

    @property
    def subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Antenatal Visit Membership'
        verbose_name_plural = 'Antenatal Visit Membership'
        consent_model = 'td_maternal.maternalconsent'
        visit_schedule_name = 'maternal_visit_schedule'
