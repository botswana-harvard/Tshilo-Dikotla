from edc_appointment.model_mixins import AppointmentModelMixin
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin


class Appointment(AppointmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    class Meta:
        consent_model = 'td_maternal.maternalconsent'
        app_label = 'td_appointment'
