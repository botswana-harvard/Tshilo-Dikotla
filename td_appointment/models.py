from edc_appointment.model_mixins import AppointmentModelMixin
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_sync.models import SyncHistoricalRecords, SyncModelMixin

from .appointment_manager import AppointmentManager


class Appointment(SyncModelMixin, AppointmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    def natural_key(self):
        return (self.subject_identifier, self.visit_code)

    objects = AppointmentManager()

    history = SyncHistoricalRecords()

    class Meta:
        app_label = 'td_appointment'
        consent_model = 'td_maternal.maternalconsent'
