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

    @property
    def str_pk(self):
        return str(self.pk)

    @property
    def maternal_visit(self):
        from td_maternal.models.maternal_visit import MaternalVisit
        try:
            return MaternalVisit.objects.get(appointment=self)
        except MaternalVisit.DoesNotExist:
            return None

    class Meta:
        app_label = 'td_appointment'
        consent_model = 'td_maternal.maternalconsent'
