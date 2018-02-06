from django.db import models

from edc_appointment.models import AppointmentMixin
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_base.model.validators.date import date_not_future
from edc_constants.choices import GENDER_UNDETERMINED
from edc_export.models import ExportTrackingFieldsMixin
from edc_offstudy.models import OffStudyMixin
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords

from td_maternal.models import MaternalLabourDel

from ..managers import InfantBirthModelManager
from td_maternal.models.maternal_consent import MaternalConsent
from edc_appointment.exceptions import AppointmentCreateError
from edc_visit_schedule.models.visit_definition import VisitDefinition
from edc_visit_schedule.models.schedule import Schedule


class InfantBirth(SyncModelMixin, OffStudyMixin, AppointmentMixin, ExportTrackingFieldsMixin, BaseUuidModel):
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

    history = SyncHistoricalRecords()

    def natural_key(self):
        return self.maternal_labour_del.natural_key()
    natural_key.dependencies = ['td_maternal.maternallabourdel', 'edc_registration.registered_subject']

    def __str__(self):
        return "{} ({}) {}".format(self.first_name, self.initials, self.gender)

    @property
    def group_names(self):
        return ['Infant Enrollment', 'Infant Enrollment1']

    def schedule(self, model_name=None, group_names=None):
        """Returns the schedule for this membership_form."""
        return Schedule.objects.filter(
            membership_form__content_type_map__model=model_name, group_name__in=group_names)

    def visit_definitions_for_schedule(self, model_name=None, instruction=None):
        """Returns a visit_definition queryset for this membership form's schedule."""
        # VisitDefinition = get_model('edc_visit_schedule', 'VisitDefinition')
        schedule = self.schedule(model_name=model_name, group_names=self.group_names)
        if instruction:
            visit_definitions = VisitDefinition.objects.filter(
                schedule__in=schedule, instruction=instruction).order_by('time_point')
        else:
            visit_definitions = VisitDefinition.objects.filter(
                schedule=schedule).order_by('time_point')
        if not visit_definitions:
            raise AppointmentCreateError(
                'No visit_definitions found for membership form class {0} '
                'in schedule group {1}. Expected at least one visit '
                'definition to be associated with schedule group {1}.'.format(
                    model_name, schedule))
        return visit_definitions

    def prepare_appointments(self, using):
        """Creates infant appointments relative to the date-of-delivery"""
        relative_identifier = self.registered_subject.relative_identifier
        maternal_labour_del = MaternalLabourDel.objects.get(
            registered_subject__subject_identifier=relative_identifier)
        maternal_consent = MaternalConsent.objects.filter(
                    subject_identifier=relative_identifier).order_by('version').last()
        instruction = 'V' + maternal_consent.version
        self.create_all(
            base_appt_datetime=maternal_labour_del.delivery_datetime, using=using, instruction=instruction)

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Birth"
