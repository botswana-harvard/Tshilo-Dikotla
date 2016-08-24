from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_call_manager.managers import CallManager, LogManager, LogEntryManager
from edc_call_manager.models import CallModelMixin, LogModelMixin, LogEntryModelMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords


class Call(SyncModelMixin, CallModelMixin, BaseUuidModel):

    history = SyncHistoricalRecords()

    objects = CallManager()

    class Meta(CallModelMixin.Meta):
        app_label = 'td_call_manager'


class Log(SyncModelMixin, LogModelMixin, BaseUuidModel):

    call = models.ForeignKey(Call)

    history = SyncHistoricalRecords()

    objects = LogManager()

    class Meta(LogModelMixin.Meta):
        app_label = 'td_call_manager'


class LogEntry(SyncModelMixin, LogEntryModelMixin, BaseUuidModel):

    log = models.ForeignKey(Log)

    history = SyncHistoricalRecords()

    objects = LogEntryManager()

    class Meta(LogEntryModelMixin.Meta):
        app_label = 'td_call_manager'
