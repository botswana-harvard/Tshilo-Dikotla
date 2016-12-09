from django.apps import apps as django_apps

from edc_appointment.managers import AppointmentManager
from edc_base.model.models import HistoricalRecords, BaseUuidModel, UrlMixin
from edc_appointment.model_mixins import AppointmentModelMixin


class Appointment(AppointmentModelMixin, UrlMixin, BaseUuidModel):

    objects = AppointmentManager()

    history = HistoricalRecords()

    @property
    def visit(self):
        MaternalVisit = django_apps.get_model('td_maternal', 'maternalvisit')
        InfantVisit = django_apps.get_model('td_infant', 'infantvisit')
        try:
            visit = MaternalVisit.objects.get(appointment=self)
        except MaternalVisit.DoesNotExist:
            try:
                visit = MaternalVisit.objects.get(appointment=self)
            except InfantVisit.DoesNotExist:
                visit = None
        return visit

    class Meta(AppointmentModelMixin.Meta):
        app_label = 'td'
