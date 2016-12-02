from django.db import models

from edc_base.model.models import BaseUuidModel, UrlMixin
from edc_consent.model_mixins import RequiresConsentMixin, SpecimenConsentMixin
from edc_consent.field_mixins import SampleCollectionFieldsMixin, VulnerabilityFieldsMixin
from edc_base.model.models import HistoricalRecords

from ..managers import EnrollmentManager


class SpecimenConsent(SpecimenConsentMixin, SampleCollectionFieldsMixin, RequiresConsentMixin,
                      VulnerabilityFieldsMixin, UrlMixin, BaseUuidModel):

    """ A model completed by the user when a mother gives consent for specimen storage. """

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        unique=True,
        editable=False)

    objects = EnrollmentManager()

    history = HistoricalRecords()

    def __str__(self):
        return "{0}".format(self.subject_identifier)

    def natural_key(self):
        return (self.subject_identifier, )

    def prepare_appointments(self, using):
        """Overrides so that the signal does not attempt to prepare appointments."""
        pass

    def get_subject_identifier(self):
        return self.subject_identifier

    def get_report_datetime(self):
        return self.consent_datetime

    @property
    def report_datetime(self):
        return self.consent_datetime

    class Meta:
        consent_model = 'td_maternal.maternalconsent'
        visit_schedule_name = 'maternal_visit_schedule'
        app_label = 'td_maternal'
        verbose_name = 'Specimen Consent'
        verbose_name_plural = 'Specimen Consent'
