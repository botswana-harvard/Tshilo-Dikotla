from django.apps import apps as django_apps

from edc_registration.models import RegisteredSubject
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_appointment.managers import AppointmentManager
from edc_base.model.models import HistoricalRecords, BaseUuidModel, UrlMixin
from edc_appointment.model_mixins import AppointmentModelMixin


class Appointment(AppointmentModelMixin, UrlMixin, BaseUuidModel):

    history = HistoricalRecords()

    objects = AppointmentManager()

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

    @property
    def appt_title(self):
        visit_schedule = site_visit_schedules.get_visit_schedule(self.visit_schedule_name)
        for _, schedule in visit_schedule.schedules.items():
            if schedule.get_visit(self.visit_code):
                return schedule.get_visit(self.visit_code).title

    @property
    def maternal_visit(self):
        MaternalVisit = django_apps.get_model('td_maternal', 'maternalvisit')
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
        app_label = 'td'
