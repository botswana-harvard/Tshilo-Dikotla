from uuid import uuid4
from django.utils import timezone

from django.db import models
from django.apps import apps
# from django.db.models import get_model

# from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_export.models import ExportTrackingFieldsMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_consent.consent_type import site_consent_types

from tshilo_dikotla.constants import MIN_AGE_OF_CONSENT, MAX_AGE_OF_CONSENT

from ..managers import MaternalEligibilityManager
from django.conf import settings


class MaternalEligibility (SyncModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):
    """ A model completed by the user to test and capture the result of the pre-consent eligibility checks.

    This model has no PII."""

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    eligibility_id = models.CharField(
        verbose_name="Eligibility Identifier",
        max_length=36,
        unique=True,
        editable=False)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        help_text='Date and time of assessing eligibility')

    age_in_years = models.IntegerField(
        verbose_name='What is the age of the participant?')

    has_omang = models.CharField(
        verbose_name="Do you have an OMANG?",
        max_length=3,
        choices=YES_NO)

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)
    # is updated via signal once subject is consented
    is_consented = models.BooleanField(
        default=False,
        editable=False)
    # updated by signal on saving consent, is determined by participant
    # citizenship
    has_passed_consent = models.BooleanField(
        default=False,
        editable=False)

    objects = MaternalEligibilityManager()

    history = SyncHistoricalRecords()

    def save(self, *args, **kwargs):
        self.set_uuid_for_eligibility_if_none()
        self.is_eligible, error_message = self.check_eligibility()
        # error_message not None if is_eligible is False
        self.ineligibility = error_message
        super(MaternalEligibility, self).save(*args, **kwargs)

    def check_eligibility(self):
        """Returns a tuple (True, None) if mother is eligible otherwise (False, error_messsage) where
        error message is the reason for eligibility test failed."""
        error_message = []
        if self.age_in_years < MIN_AGE_OF_CONSENT:
            error_message.append(
                'Mother is under {}'.format(MIN_AGE_OF_CONSENT))
        if self.age_in_years > MAX_AGE_OF_CONSENT:
            error_message.append(
                'Mother is too old (>{})'.format(MAX_AGE_OF_CONSENT))
        if self.has_omang == NO:
            error_message.append('Not a citizen')
        is_eligible = False if error_message else True
        return (is_eligible, ','.join(error_message))

    def __str__(self):
        return "Screened, age ({})".format(self.age_in_years)

    def natural_key(self):
        return self.eligibility_id

    @property
    def maternal_eligibility_loss(self):
        MaternalEligibilityLoss = apps.get_model(
            'td_maternal', 'MaternalEligibilityLoss')
        try:
            maternal_eligibility_loss = MaternalEligibilityLoss.objects.get(
                maternal_eligibility_id=self.id)
        except MaternalEligibilityLoss.DoesNotExist:
            maternal_eligibility_loss = None
        return maternal_eligibility_loss

    @property
    def have_latest_consent(self):
        MaternalConsent = apps.get_model('td_maternal', 'MaternalConsent')
        return (MaternalConsent.objects.filter(
            subject_identifier=self.registered_subject.subject_identifier).order_by('-version').first().version ==
            site_consent_types.get_by_consent_datetime(MaternalConsent, timezone.now()).version)

    @property
    def previous_consents(self):
        MaternalConsent = apps.get_model('td_maternal', 'MaternalConsent')
        return MaternalConsent.objects.filter(
            subject_identifier=self.registered_subject.subject_identifier).order_by('version')

    @property
    def latest_consent_version(self):
        MaternalConsent = apps.get_model('td_maternal', 'MaternalConsent')
        consent_type = site_consent_types.get_by_datetime_lastest_version(
            MaternalConsent, timezone.now())
        return consent_type.version

    @property
    def re_consent(self):
        if self.previous_consents and self.td_consent_version:
            MaternalConsent = apps.get_model('td_maternal', 'MaternalConsent')
            try:
                maternal_consent = MaternalConsent.objects.get(
                    subject_identifier=self.registered_subject.subject_identifier,
                    version=settings.LASTEST_VERSION)
            except MaternalConsent.DoesNotExist:
                maternal_consent = None

            if self.td_consent_version.version == settings.LASTEST_VERSION and not maternal_consent:
                return True
        return False

    @property
    def td_consent_version(self):
        """Returns a td consent version instance.
        """
        from td_maternal.models import TdConsentVersion
        try:
            td_consent_version = TdConsentVersion.objects.get(
                maternal_eligibility=self)
        except TdConsentVersion.DoesNotExist:
            td_consent_version = None
        return td_consent_version

    def set_uuid_for_eligibility_if_none(self):
        if not self.eligibility_id:
            self.eligibility_id = str(uuid4())

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Eligibility"
        verbose_name_plural = "Maternal Eligibility"
