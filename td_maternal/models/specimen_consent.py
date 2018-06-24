from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin, BaseSpecimenConsent
from edc_consent.models.fields import SampleCollectionFieldsMixin, VulnerabilityFieldsMixin
from edc_export.models import ExportTrackingFieldsMixin
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncHistoricalRecords

from ..managers import SpecimenConsentManager

from .maternal_consent import MaternalConsent
from td_appoinement_mixin import TdAppointmentMixin


class SpecimenConsent(BaseSpecimenConsent, SampleCollectionFieldsMixin, RequiresConsentMixin,
                      VulnerabilityFieldsMixin, TdAppointmentMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    """ A model completed by the user when a mother gives consent for specimen storage. """

    consent_model = MaternalConsent

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    objects = SpecimenConsentManager()

    history = SyncHistoricalRecords()

    def __str__(self):
        return "{0}".format(self.registered_subject.subject_identifier)

    def natural_key(self):
        return self.registered_subject.natural_key()

    def prepare_appointments(self, using):
        """Overrides so that the signal does not attempt to prepare appointments."""
        pass

    @property
    def group_names(self):
        return ['Specimen Consent']

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_report_datetime(self):
        return self.consent_datetime

    @property
    def subject_identifier(self):
        return self.get_subject_identifier()
#     subject_identifier.allow_tags = True

    @property
    def report_datetime(self):
        return self.consent_datetime

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Specimen Consent'
        verbose_name_plural = 'Specimen Consent'
