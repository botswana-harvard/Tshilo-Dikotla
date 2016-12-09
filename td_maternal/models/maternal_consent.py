from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db import models

from edc_base.model.fields import OtherCharField
from edc_base.model.models import BaseUuidModel, UrlMixin, HistoricalRecords
from edc_consent.field_mixins import (
    PersonalFieldsMixin, CitizenFieldsMixin, ReviewFieldsMixin, VulnerabilityFieldsMixin,
    IdentityFieldsMixin)
from edc_consent.model_mixins import ConsentModelMixin
from edc_identifier.maternal_identifier import MaternalIdentifier
from edc_protocol.mixins import SubjectTypeCapMixin
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin

from ..managers import MaternalConsentManager
from ..choices import RECRUIT_SOURCE, RECRUIT_CLINIC

from .maternal_eligibility import MaternalEligibility


class MaternalConsent(ConsentModelMixin, UpdatesOrCreatesRegistrationModelMixin, ReviewFieldsMixin,
                      IdentityFieldsMixin, PersonalFieldsMixin,
                      CitizenFieldsMixin, VulnerabilityFieldsMixin,
                      SubjectTypeCapMixin, UrlMixin, BaseUuidModel):

    """ A model completed by the user on the mother's consent. """

    ADMIN_SITE_NAME = 'td_maternal_admin'

    maternal_eligibility_reference = models.UUIDField()

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
        null=True)

    objects = MaternalConsentManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.subject_identifier, self.first_name, self.dob, self.initials, self.version,)

    def save(self, *args, **kwargs):
        try:
            MaternalEligibility.objects.get(reference=self.maternal_eligibility_reference)
        except MaternalEligibility.DoesNotExist:
            ValidationError('Unable to determine eligibility criteria. Was Maternal Eligibility completed?')
        if not self.id:
            try:
                RegisteredSubject = django_apps.get_app_config('edc_registration').model
                registered_subject = RegisteredSubject.objects.get(identity=self.identity)
                self.subject_identifier = registered_subject.subject_identifier
            except RegisteredSubject.DoesNotExist:
                maternal_identifier = MaternalIdentifier(
                    subject_type_name='maternal',
                    model=self._meta.label_lower,
                    study_site=self.study_site,
                    create_registration=False)
                self.subject_identifier = maternal_identifier.identifier
        super(MaternalConsent, self).save(*args, **kwargs)

    def get_registration_datetime(self):
        return self.consent_datetime

    def registration_update_or_create(self):
        """Updates or Creates RegisteredSubject on the post-save signal."""
        super(MaternalConsent, self).registration_update_or_create()
        RegisteredSubject = django_apps.get_app_config('edc_registration').model
        maternal_eligibility = MaternalEligibility.objects.get(reference=self.maternal_eligibility_reference)
        registered_subject = RegisteredSubject.objects.get(subject_identifier=self.subject_identifier)
        registered_subject.screening_identifier = maternal_eligibility.reference
        registered_subject.screening_datetime = maternal_eligibility.report_datetime
        registered_subject.screening_age_in_years = maternal_eligibility.age_in_years
        registered_subject.save()

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Maternal Consent'
        unique_together = ('subject_identifier', 'first_name', 'dob', 'initials', 'version')
