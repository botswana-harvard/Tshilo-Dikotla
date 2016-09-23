from django.core.validators import RegexValidator
from django.db import models
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.field_mixins import (
    ReviewFieldsMixin, PersonalFieldsMixin, VulnerabilityFieldsMixin, CitizenFieldsMixin)
from edc_constants.choices import GENDER
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords

from django_crypto_fields.fields import IdentityField, FirstnameField, LastnameField, EncryptedCharField


class PotentialCallManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class PotentialCall(SyncModelMixin, BaseUuidModel):

    approximate_date = models.DateField(
        verbose_name="approximate appointment date",
        help_text='This date can be modified.')

    visit_code = models.CharField(
        max_length=10)

    identity = IdentityField(
        verbose_name="Identity",
        help_text=("Use Omang, Passport number, driver's license number or Omang receipt number")
    )

    subject_identifier = models.CharField(
        max_length=25)

    first_name = FirstnameField(
        null=True,
    )

    last_name = LastnameField(
        verbose_name="Last name",
        null=True,
    )

    initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message=('Ensure initials consist of letters '
                     'only in upper case, no spaces.')), ],
        null=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER,
        null=True)

    dob = models.DateField(null=True)

    contacted = models.BooleanField(default=False, editable=False)

    history = SyncHistoricalRecords()

    objects = PotentialCallManager()

    def natural_key(self):
        return (self.subject_identifier, )

    @property
    def subject_consent(self):
        from .maternal_consent import MaternalConsent
        try:
            subject_consent = MaternalConsent.objects.get(subject_identifier=self.subject_identifier)
        except MaternalConsent.DoesNotExist:
            return None
        return subject_consent

    def __str__(self):
        from .maternal_consent import MaternalConsent
        try:
            subject_consent = MaternalConsent.objects.get(potential_call=self)
            first_name = subject_consent.first_name
            last_name = subject_consent.last_name
            name = first_name + ' ' + last_name
        except MaternalConsent.DoesNotExist:
            name = 'not consented'
        return '{}. {}'.format(
            name, self.subject_identifier)

    class Meta:
        app_label = 'td_maternal'
        unique_together = ('visit_code', 'subject_identifier')
