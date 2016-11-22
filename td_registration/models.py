from django.db import models
from edc_base.model.models import BaseUuidModel
from edc_registration.model_mixins import RegisteredSubjectModelMixin
from edc_base.model.models import HistoricalRecords
from edc_registration.managers import RegisteredSubjectManager


class RegisteredSubject(RegisteredSubjectModelMixin, BaseUuidModel):

    subject_type = models.CharField(
        max_length=25,
        blank=True,
        null=True)

    objects = RegisteredSubjectManager()

    history = HistoricalRecords()

    class Meta:
        app_label = 'td_registration'
