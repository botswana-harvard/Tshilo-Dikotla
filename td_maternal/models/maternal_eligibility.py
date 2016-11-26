from uuid import uuid4
from django.utils import timezone

from django.db import models
from django.apps import apps

from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_future
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_base.model.models import HistoricalRecords
from edc_consent.site_consents import site_consents
from edc_protocol.validators import datetime_not_before_study_start

from td.constants import MIN_AGE_OF_CONSENT, MAX_AGE_OF_CONSENT

from ..managers import MaternalEligibilityManager
from edc_base.model.models.url_mixin import UrlMixin


def getuuid():
    return str(uuid4())


class MaternalEligibility (UrlMixin, BaseUuidModel):
    """ A model completed by the user to test and capture the result of the pre-consent eligibility checks.

    This model has no PII."""

    eligibility_id = models.CharField(
        verbose_name="Eligibility Identifier",
        max_length=36,
        unique=True,
        default=getuuid,
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
    # updated by signal on saving consent, is determined by participant citizenship
    has_passed_consent = models.BooleanField(
        default=False,
        editable=False)

    objects = MaternalEligibilityManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.is_eligible, error_message = self.check_eligibility()
        self.ineligibility = error_message  # error_message not None if is_eligible is False
        super(MaternalEligibility, self).save(*args, **kwargs)

    def check_eligibility(self):
        """Returns a tuple (True, None) if mother is eligible otherwise (False, error_messsage) where
        error message is the reason for eligibility test failed."""
        error_message = []
        if self.age_in_years < MIN_AGE_OF_CONSENT:
            error_message.append('Mother is under {}'.format(MIN_AGE_OF_CONSENT))
        if self.age_in_years > MAX_AGE_OF_CONSENT:
            error_message.append('Mother is too old (>{})'.format(MAX_AGE_OF_CONSENT))
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
        MaternalEligibilityLoss = apps.get_model('td_maternal', 'MaternalEligibilityLoss')
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
            site_consents.get_by_datetime(MaternalConsent, timezone.now()).version)

    @property
    def previous_consents(self):
        MaternalConsent = apps.get_model('td_maternal', 'MaternalConsent')
        return MaternalConsent.objects.filter(
            subject_identifier=self.registered_subject.subject_identifier).order_by('version')

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Eligibility"
        verbose_name_plural = "Maternal Eligibility"
