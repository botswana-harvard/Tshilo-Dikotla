from django.db import models
from edc_base.model.models import BaseUuidModel
from edc_registration.model_mixins import RegisteredSubjectModelMixin
from edc_sync.models import SyncHistoricalRecords, SyncModelMixin


class RegisteredSubject(SyncModelMixin, RegisteredSubjectModelMixin, BaseUuidModel):

    subject_type = models.CharField(
        max_length=25,
        blank=True,
        null=True)

    history = SyncHistoricalRecords()

    class Meta:
        app_label = 'td_registration'
