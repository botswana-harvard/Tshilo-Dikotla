from django.db import models
from django.apps import apps as django_apps

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_future
from edc_protocol.validators import datetime_not_before_study_start
from edc_base.model.validators.date import date_not_future
from edc_constants.choices import GENDER_UNDETERMINED
from edc_export.model_mixins import ExportTrackingFieldsMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from td.models import RegisteredSubject
from edc_base.model.models import HistoricalRecords

from td_maternal.models import MaternalLabourDel

from ..managers import InfantBirthModelManager
from edc_base.model.models.url_mixin import UrlMixin


class InfantBirth(CreateAppointmentsMixin, UpdatesOrCreatesRegistrationModelMixin, ExportTrackingFieldsMixin,
                  OffstudyMixin, UrlMixin, BaseUuidModel):
    """ A model completed by the user on the infant's birth. """

    off_study_model = ('td_infant', 'InfantOffStudy')

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    maternal_labour_del = models.ForeignKey(
        MaternalLabourDel,
        verbose_name="Mother's delivery record")

    report_datetime = models.DateTimeField(
        verbose_name="Date and Time infant enrolled",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    first_name = models.CharField(
        max_length=25,
        verbose_name="Infant's first name",
        help_text="If infant name is unknown or not yet determined, "
                  "use Baby + birth order + mother's last name, e.g. 'Baby1Malane'")

    initials = models.CharField(
        max_length=3)

    dob = models.DateField(
        verbose_name='Date of Birth',
        help_text="Must match labour and delivery report.",
        validators=[date_not_future, ])

    gender = models.CharField(
        max_length=10,
        choices=GENDER_UNDETERMINED)

    objects = InfantBirthModelManager()

    history = HistoricalRecords()

#     @property
#     def subject_identifier(self):
#         return self.registered_subject.subject_identifier

    def natural_key(self):
        return self.maternal_labour_del.natural_key()
    natural_key.dependencies = ['td_maternal.maternallabourdel', 'td.registered_subject']

    def __str__(self):
        return "{} ({}) {}".format(self.first_name, self.initials, self.gender)

#     def prepare_appointments(self, using):
#         """Creates infant appointments relative to the date-of-delivery"""
#         relative_identifier = self.registered_subject.relative_identifier
#         maternal_labour_del = MaternalLabourDel.objects.get(
#             registered_subject__subject_identifier=relative_identifier)
#         self.create_all(
#             base_appt_datetime=maternal_labour_del.delivery_datetime, using=using)

    @property
    def visit(self):
        return getattr(self, 'infant_visit')

    @property
    def registration_instance(self):
        registration_instance = None
        try:
            model = django_apps.get_app_config('edc_registration').model
            registration_instance = model.objects.get(subject_identifier=self.get_subject_identifier())
        except model.DoesNotExist as e:
            raise model.DoesNotExist('{} subject_identifier=\'{}\''.format(str(e), self.subject_identifier))
        return registration_instance

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Birth"
#         consent_model = 'td_maternal.maternalconsent'
        visit_schedule_name = 'infant_visit_schedule'
