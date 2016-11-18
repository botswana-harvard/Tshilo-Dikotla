from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_call_manager.managers import CallManager, LogManager, LogEntryManager
from edc_call_manager.models import CallModelMixin, LogModelMixin, LogEntryModelMixin
from edc_base.model.models import HistoricalRecords


class Call(CallModelMixin, BaseUuidModel):

    history = HistoricalRecords()

    objects = CallManager()

    class Meta(CallModelMixin.Meta):
        app_label = 'td_call_manager'


class Log(LogModelMixin, BaseUuidModel):

    call = models.ForeignKey(Call)

    history = HistoricalRecords()

    objects = LogManager()

    class Meta(LogModelMixin.Meta):
        app_label = 'td_call_manager'


class LogEntry(LogEntryModelMixin, BaseUuidModel):

    log = models.ForeignKey(Log)

    history = HistoricalRecords()

    objects = LogEntryManager()

    class Meta(LogEntryModelMixin.Meta):
        app_label = 'td_call_manager'
