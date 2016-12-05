from uuid import uuid4

from django.db import models
from django.apps import apps

from edc_base.model.models import BaseUuidModel, UrlMixin
from edc_base.model.validators import datetime_not_future
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_base.model.models import HistoricalRecords
from edc_consent.site_consents import site_consents
from edc_protocol.validators import datetime_not_before_study_start

from ..managers import MaternalEligibilityManager
from td_maternal.models.maternal_eligibility_loss import MaternalEligibilityLoss


class MaternalEligibility (UrlMixin, BaseUuidModel):
    """ A model completed by the user to test and capture the result of the pre-consent eligibility checks.

    This model has no PII."""

    reference_pk = models.UUIDField(
        verbose_name="Anonymous Reference",
        unique=True,
        default=uuid4,
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
        self.is_eligible, self.ineligibility = self.get_is_eligible()
        super(MaternalEligibility, self).save(*args, **kwargs)

    def get_is_eligible(self):
        """Returns a tuple (True, None) if mother is eligible otherwise (False, error_messsage) where
        error message is the reason for eligibility test failed."""
        error_message = []
        consent_config = site_consents.get_consent_config(
            'td_maternal.maternalconsent', report_datetime=self.report_datetime)
        if self.age_in_years < consent_config.age_min:
            error_message.append('Mother is under {}'.format(consent_config.age_min))
        if self.age_in_years > consent_config.age_max:
            error_message.append('Mother is too old (>{})'.format(consent_config.age_max))
        if self.has_omang == NO:
            error_message.append('Not a citizen')
        is_eligible = False if error_message else True
        return (is_eligible, ','.join(error_message))

    def __str__(self):
        return "Screened, age ({})".format(self.age_in_years)

    def natural_key(self):
        return self.eligibility_id

    @property
    def is_consented(self):
        return True if self.previous_consents else False

    @property
    def previous_consents(self):
        MaternalConsent = apps.get_model('td_maternal', 'MaternalConsent')
        return MaternalConsent.objects.filter(maternal_eligibility_reference=self.reference_pk).order_by('version')

    def create_update_or_delete_eligibility_loss(self):
        if self.is_eligible:
            MaternalEligibilityLoss.objects.filter(maternal_eligibility_reference=self.reference_pk).delete()
        else:
            try:
                maternal_eligibility_loss = MaternalEligibilityLoss.objects.get(
                    maternal_eligibility_reference=self.reference_pk)
                maternal_eligibility_loss.report_datetime = self.report_datetime
                maternal_eligibility_loss.reason_ineligible = self.ineligibility
                maternal_eligibility_loss.user_modified = self.user_modified
                maternal_eligibility_loss.save()
            except MaternalEligibilityLoss.DoesNotExist:
                MaternalEligibilityLoss.objects.create(
                    maternal_eligibility_reference=self.reference_pk,
                    report_datetime=self.report_datetime,
                    reason_ineligible=self.ineligibility,
                    user_created=self.user_created,
                    user_modified=self.user_modified)

    @property
    def maternal_eligibility_loss(self):
        MaternalEligibilityLoss = apps.get_model('td_maternal', 'MaternalEligibilityLoss')
        try:
            maternal_eligibility_loss = MaternalEligibilityLoss.objects.get(
                maternal_eligibility_reference=self.reference_pk)
        except MaternalEligibilityLoss.DoesNotExist:
            maternal_eligibility_loss = None
        return maternal_eligibility_loss

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Eligibility"
        verbose_name_plural = "Maternal Eligibility"
