from django.db import models

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
from td_appoinement_mixin import TdAppointmentMixin


class AntenatalVisitMembership(SyncModelMixin, RequiresConsentMixin,
                               TdAppointmentMixin, ExportTrackingFieldsMixin, BaseUuidModel):

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

    def prepare_appointments(self, using):
        """Creates infant appointments relative to the date-of-delivery"""
        maternal_consent = MaternalConsent.objects.filter(
                    subject_identifier=self.subject_identifier).order_by('version').last()
        instruction = 'V' + maternal_consent.version
        self.create_all(using=using, instruction=instruction)

    @property
    def group_names(self):
        return ['Antenatal Visit', 'Antenatal Visit v3']

    @property
    def subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Antenatal Visit Membership'
        verbose_name_plural = 'Antenatal Visit Membership'
