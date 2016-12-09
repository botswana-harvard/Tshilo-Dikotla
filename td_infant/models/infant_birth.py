from django.db import models

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords, UrlMixin
from edc_base.model.validators import datetime_not_future
from edc_offstudy.model_mixins import OffstudyMixin
from edc_pregnancy_utils.model_mixins import BirthModelMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_visit_schedule.model_mixins import EnrollmentModelMixin


from ..managers import InfantBirthModelManager


class InfantBirth(BirthModelMixin, EnrollmentModelMixin, CreateAppointmentsMixin,
                  OffstudyMixin, UrlMixin, BaseUuidModel):
    """ A model completed by the user on the infant's birth. """

    report_datetime = models.DateTimeField(
        verbose_name="Date and Time infant enrolled",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    objects = InfantBirthModelManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.subject_identifier, )

    def __str__(self):
        return "{} ({}) {}".format(self.first_name, self.initials, self.gender)

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Birth"
        visit_schedule_name = 'infant_visit_schedule.infant_birth'
        delivery_model = 'td_maternal.maternallabdel'
        unique_together = (
            ('subject_identifier', 'visit_schedule_name', 'schedule_name'),
            ('delivery_reference', 'birth_order', 'birth_order_denominator'),
            ('delivery_reference', 'birth_order', 'birth_order_denominator', 'first_name')
        )
