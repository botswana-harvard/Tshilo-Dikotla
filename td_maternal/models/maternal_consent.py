from django.conf import settings
from django.db import models

from edc_base.model.fields import OtherCharField
from edc_base.model.models import BaseUuidModel
from edc_consent.models.base_consent import BaseConsent
from edc_consent.models.fields import (
    PersonalFieldsMixin, CitizenFieldsMixin, ReviewFieldsMixin, VulnerabilityFieldsMixin)
from edc_consent.models.fields.bw import IdentityFieldsMixin
from edc_export.models import ExportTrackingFieldsMixin
from edc_identifier.subject.classes import SubjectIdentifier
from edc_offstudy.models import OffStudyMixin
from edc_sync.models import SyncModelMixin

from tshilo_dikotla.constants import MIN_AGE_OF_CONSENT, MAX_AGE_OF_CONSENT

from ..maternal_choices import RECRUIT_SOURCE, RECRUIT_CLINIC

from .maternal_eligibility import MaternalEligibility
from edc_consent.consent_type import site_consent_types
from edc_consent.exceptions import ConsentVersionError
from td_maternal.models.td_consent_version import TdConsentVersion


class MaternalConsent(BaseConsent, SyncModelMixin, OffStudyMixin, ReviewFieldsMixin,
                      IdentityFieldsMixin, PersonalFieldsMixin,
                      CitizenFieldsMixin, VulnerabilityFieldsMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    """ A model completed by the user on the mother's consent. """

    MIN_AGE_OF_CONSENT = MIN_AGE_OF_CONSENT
    MAX_AGE_OF_CONSENT = MAX_AGE_OF_CONSENT

    off_study_model = 'td_maternal.maternaloffstudy'

    visit_model_attr = 'maternal_visit'

    maternal_eligibility = models.ForeignKey(MaternalEligibility)

    recruit_source = models.CharField(
        max_length=75,
        choices=RECRUIT_SOURCE,
        verbose_name="The mother first learned about the tshilo dikotla study from ")

    recruit_source_other = OtherCharField(
        max_length=35,
        verbose_name="if other recruitment source, specify...",
        blank=True,
        null=True)

    recruitment_clinic = models.CharField(
        max_length=100,
        verbose_name="The mother was recruited from",
        choices=RECRUIT_CLINIC)

    recruitment_clinic_other = models.CharField(
        max_length=100,
        verbose_name="if other recruitment clinic, specify...",
        blank=True,
        null=True, )

#     history = AuditTrail()

    def __str__(self):
        return '{0} {1} {2} ({3})'.format(self.subject_identifier, self.first_name,
                                          self.last_name, self.initials)

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields')
        previous_consent = self.__class__.objects.filter(
            maternal_eligibility=self.maternal_eligibility)
        if not self.id and previous_consent.exists():
            self.subject_identifier = previous_consent.first().subject_identifier
        elif not self.id:
            self.subject_identifier = SubjectIdentifier(
                site_code=self.study_site).get_identifier()
        if previous_consent:
            consent_type = site_consent_types.get_by_consent_datetime(
                self.__class__, self.consent_datetime,
                version=self.td_consent_version(previous_consent=previous_consent, update_fields=update_fields))
        else:
            consent_type = site_consent_types.get_by_datetime_lastest_version(
                self.__class__, self.consent_datetime)
        self.raise_error_if_reconsent_not_required(
            previous_consent=previous_consent)
        self.version = consent_type.version
        if consent_type.updates_version:
            try:
                previous_consent = self.__class__.objects.get(
                    subject_identifier=self.subject_identifier,
                    identity=self.identity,
                    version__in=consent_type.updates_version,
                    **self.additional_filter_options())
                previous_consent.subject_identifier_as_pk = self.subject_identifier_as_pk
                previous_consent.subject_identifier_aka = self.subject_identifier_aka
            except self.__class__.DoesNotExist:
                raise ConsentVersionError(
                    'Previous consent with version {0} for this subject not found. Version {1} updates {0}.'
                    'Ensure all details match (identity, dob, first_name, last_name)'.format(
                        consent_type.updates_version, self.version))
        super(MaternalConsent, self).save(*args, **kwargs)

    def raise_error_if_reconsent_not_required(self, previous_consent=None):
        """Raise an error if re-consenting is not required"""
        if previous_consent and (self.td_consent_version(previous_consent=previous_consent) == settings.PREVIOUS_CONSENT_VERSION) and not self.id:
            raise ConsentVersionError(
                "Re Consenting declided by participant as per the TdConsentVersion form")

    def get_registration_datetime(self):
        return self.consent_datetime

    def td_consent_version(self, previous_consent=None, update_fields=None):
        try:
            td_consent_version = TdConsentVersion.objects.get(
                maternal_eligibility=self.maternal_eligibility)
        except TdConsentVersion.DoesNotExist:
            if previous_consent and 'is_verified' not in update_fields:
                raise ConsentVersionError(
                    "Please fill in the TD consent version form first.")
        else:
            return td_consent_version.version

    def get_subject_identifier(self):
        return self.subject_identifier

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Maternal Consent'
        unique_together = ('first_name', 'dob', 'initials', 'version')
