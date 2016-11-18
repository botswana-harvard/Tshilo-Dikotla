from django.db import models
from edc_base.model.models import BaseUuidModel
from edc_registration.model_mixins import RegisteredSubjectModelMixin
from edc_base.model.models import HistoricalRecords
from edc_registration.managers import RegisteredSubjectManager


class TdRegisteredSubjectManager(RegisteredSubjectManager):

    def get_for_subject_identifier(self, subject_identifier):
        """Returns a queryset for the given subject_identifier."""
        options = {'subject_identifier': subject_identifier}
        return self.filter(**options)

    def get_for_visit(self, visit):
        options = {'subject_identifier': visit.subject_identifier}
        return self.get(**options)


class RegisteredSubject(RegisteredSubjectModelMixin, BaseUuidModel):

    objects = TdRegisteredSubjectManager()

    subject_type = models.CharField(
        max_length=25,
        blank=True,
        null=True)

    history = HistoricalRecords()

    class Meta:
        app_label = 'td_registration'
