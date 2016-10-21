from django.urls import reverse

from edc_appointment.model_mixins import AppointmentModelMixin
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_sync.models import SyncHistoricalRecords, SyncModelMixin

from .appointment_manager import AppointmentManager
from edc_visit_schedule.site_visit_schedules import site_visit_schedules


class Appointment(SyncModelMixin, AppointmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    def natural_key(self):
        return (self.subject_identifier, self.visit_code)

    objects = AppointmentManager()

    history = SyncHistoricalRecords()

    @property
    def str_pk(self):
        return str(self.pk)

    @property
    def appt_title(self):
        visit_schedule = site_visit_schedules.get_visit_schedule(self.visit_schedule_name)
        for _, schedule in visit_schedule.schedules.items():
            if schedule.get_visit(self.visit_code):
                return schedule.get_visit(self.visit_code).title

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
