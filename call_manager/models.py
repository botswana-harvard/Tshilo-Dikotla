from django.utils import timezone
from django.db import models
from edc_sync.models import SyncHistoricalRecords

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_call_manager.managers import CallManager, LogManager, LogEntryManager
from edc_call_manager.models import CallModelMixin, LogModelMixin, LogEntryModelMixin
from edc_sync.models.sync_model_mixin import SyncModelMixin
from edc_registration.models.registered_subject_model_mixin import RegisteredSubject


class Call(SyncModelMixin, CallModelMixin, BaseUuidModel):

    registered_subject = models.ForeignKey(RegisteredSubject)

    call_datetime = models.DateTimeField(
        default=timezone.now(),
        verbose_name='Date of this call')

    history = SyncHistoricalRecords()

    objects = CallManager()

    def __str__(self):
        return self.registered_subject.subject_identifier

    @property
    def subject(self):
        return self

    def get_gender_display(self):
        return self.registered_subject.gender

    @property
    def dob(self):
        return self.registered_subject.dob

    @property
    def last_name(self):
        return self.registered_subject.last_name

    class Meta:
        app_label = 'call_manager'


class Log(SyncModelMixin, LogModelMixin, BaseUuidModel):

    call = models.ForeignKey(Call)

    history = SyncHistoricalRecords()

    objects = LogManager()

    class Meta:
        app_label = 'call_manager'


class LogEntry(SyncModelMixin, LogEntryModelMixin, BaseUuidModel):

    log = models.ForeignKey(Log)

    history = SyncHistoricalRecords()

    objects = LogEntryManager()

    class Meta:
        app_label = 'call_manager'

