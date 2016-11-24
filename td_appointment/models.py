from django.urls import reverse

from edc_appointment.model_mixins import AppointmentModelMixin
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_base.model.models import HistoricalRecords

from .appointment_manager import AppointmentManager
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from td_registration.models import RegisteredSubject


class Appointment(AppointmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    objects = AppointmentManager()

    history = HistoricalRecords()

    @property
    def str_pk(self):
        return str(self.pk)

    def natural_key(self):
        return (self.subject_identifier, self.visit_code)

    @property
    def infant_registered_subject(self):
        try:
            RegisteredSubject.objects.get(
                subject_identifier=self.subject_identifier,
                subject_type='infant'
            )
        except RegisteredSubject.DoesNotExist:
            return False
        return True

    def consented_for_period_or_raise(self, report_datetime=None, subject_identifier=None, exception_cls=None):
        if not self.infant_registered_subject:
            super().consented_for_period_or_raise(report_datetime, subject_identifier, exception_cls)

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

    @property
    def infant_visit(self):
        from td_infant.models import InfantVisit
        try:
            return InfantVisit.objects.get(appointment=self)
        except InfantVisit.DoesNotExist:
            return None

    class Meta:
        app_label = 'td_appointment'
        consent_model = 'td_maternal.maternalconsent'
