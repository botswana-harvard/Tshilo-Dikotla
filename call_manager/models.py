from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from edc_sync.models import SyncHistoricalRecords

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_call_manager.constants import NO_CONTACT
from edc_call_manager.managers import CallManager, LogManager, LogEntryManager
from edc_call_manager.models import CallModelMixin, LogModelMixin, LogEntryModelMixin
from edc_sync.models.sync_model_mixin import SyncModelMixin

from td_maternal.models import PotentialCall


class Call(SyncModelMixin, CallModelMixin, BaseUuidModel):

    potential_call = models.ForeignKey(PotentialCall)

    history = SyncHistoricalRecords()

    objects = CallManager()

    def __str__(self):
        return self.subject_identifier

    @property
    def subject(self):
        return self.potential_call

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


@receiver(post_save, sender=LogEntry, dispatch_uid='post_save_tshilo_dikotla_call')
def post_save_tshilo_dikotla_call(sender, instance, raw, created, using, update_fields, **kwargs):
    if not raw:
        if instance.contact_type != NO_CONTACT:
            instance.log.call.potential_call.contacted = True
            instance.log.call.potential_call.save(update_fields=['contacted', 'modified'])
