from django.utils import timezone
from django.db import models

from edc_appointment.models import AppointmentMixin
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_constants.choices import YES_NO
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_registration.models import RegisteredSubject

from ..maternal_choices import CALL_REASON, CONTACT_TYPE

from .maternal_consent import MaternalConsent


class MaternalContactManager(models.Manager):

    def get_by_natural_key(self, registered_subject):
        return self.get(subject_identifier=registered_subject.subject_identifier)


class MaternalContact(AppointmentMixin, SyncModelMixin, BaseUuidModel):

    consent_model = MaternalConsent

    report_datetime = models.DateTimeField(
        verbose_name='Report Date',
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=timezone.now,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    registered_subject = models.ForeignKey(RegisteredSubject)

    contact_type = models.CharField(
        verbose_name='Type of contact',
        choices=CONTACT_TYPE,
        max_length=25,
    )

    contact_datetime = models.DateTimeField(
        verbose_name='Contact datetime',
        help_text='This date can be modified.',
        null=True,
        blank=True)

    visit_code = models.CharField(
        max_length=10)

    call_reason = models.CharField(
        verbose_name='Reason for call',
        max_length=25,
        choices=CALL_REASON,
    )

    call_reason_other = models.CharField(
        verbose_name='Other, specify',
        max_length=25,
        null=True,
        blank=True
    )

    contact_success = models.CharField(
        verbose_name='Were you able to reach the participant?',
        max_length=5,
        choices=YES_NO,
        help_text='If Yes, please answer the next question.'
    )

    contact_comment = models.TextField(
        verbose_name='Outcome of call',
        max_length=150,
        null=True,
        blank=True
    )

    history = SyncHistoricalRecords()

    objects = MaternalContactManager()

    def natural_key(self):
        return (self.registered_subject.subject_identifier, )

    def prepare_appointments(self, using):
        """Overrides so that the signal does not attempt to prepare appointments."""
        pass

#     @property
#     def subject_consent(self):
#         try:
#             subject_consent = MaternalConsent.objects.get(subject_identifier=self.subject_identifier)
#         except MaternalConsent.DoesNotExist:
#             return None
#         return subject_consent

    def __str__(self):
        try:
            name = self.registered_subject.first_name
        except MaternalConsent.DoesNotExist:
            name = 'not consented'
        return '{}. {}'.format(
            name, self.registered_subject.subject_identifier)

    class Meta:
        app_label = 'td_maternal'
        unique_together = ('visit_code', 'registered_subject', 'contact_datetime')
