from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_base.model.models import BaseUuidModel
from edc_consent.models.base_consent import BaseConsent
from edc_consent.models.fields import (
    PersonalFieldsMixin, CitizenFieldsMixin, ReviewFieldsMixin, VulnerabilityFieldsMixin)
from edc_consent.models.fields.bw import IdentityFieldsMixin
from edc_export.models import ExportTrackingFieldsMixin
from edc_identifier.subject.classes import SubjectIdentifier
from edc_offstudy.models import OffStudyMixin
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin

from tshilo_dikotla.apps.td.constants import MIN_AGE_OF_CONSENT, MAX_AGE_OF_CONSENT

from ..maternal_choices import RECRUIT_SOURCE, RECRUIT_CLINIC


class MaternalConsent(BaseConsent, SyncModelMixin, OffStudyMixin, ReviewFieldsMixin,
                      IdentityFieldsMixin, PersonalFieldsMixin,
                      CitizenFieldsMixin, VulnerabilityFieldsMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    """ A model completed by the user on the mother's consent. """

    MIN_AGE_OF_CONSENT = MIN_AGE_OF_CONSENT
    MAX_AGE_OF_CONSENT = MAX_AGE_OF_CONSENT

    off_study_model = ('td_maternal', 'MaternalOffStudy')

    registered_subject = models.ForeignKey(RegisteredSubject, null=True)

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

    history = AuditTrail()

    def __unicode__(self):
        return '{0} {1} {2} ({3})'.format(self.subject_identifier, self.first_name,
                                          self.last_name, self.initials)

    def save(self, *args, **kwargs):
        previous_consent = self.__class__.objects.filter(registered_subject=self.registered_subject)
        if not self.id and previous_consent.exists():
            self.subject_identifier = previous_consent.first().subject_identifier
        elif not self.id:
            self.subject_identifier = SubjectIdentifier(
                site_code=self.study_site).get_identifier()
        super(MaternalConsent, self).save(*args, **kwargs)

    def get_registration_datetime(self):
        return self.consent_datetime

    def get_subject_identifier(self):
        return self.subject_identifier

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Maternal Consent'
