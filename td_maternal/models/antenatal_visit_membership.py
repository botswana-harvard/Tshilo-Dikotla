from django.db import models

from edc_appointment.models import AppointmentMixin
# from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future,
                                       date_not_before_study_start, date_not_future)
from edc_export.models import ExportTrackingFieldsMixin
from edc_consent.models import RequiresConsentMixin
from edc_constants.choices import YES_NO
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords

from ..managers import AntenatalVisitMembershipManager

from .maternal_consent import MaternalConsent


class AntenatalVisitMembership(SyncModelMixin, RequiresConsentMixin,
                               AppointmentMixin, ExportTrackingFieldsMixin, BaseUuidModel):

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

    history = SyncHistoricalRecords()

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
