from django.db import models
from django.db.models.deletion import PROTECT

from edc_base.model.models import UrlMixin, BaseUuidModel, HistoricalRecords
from edc_constants.constants import (DEAD, MALE)
from edc_export.model_mixins import ExportTrackingFieldsMixin
from edc_metadata.model_mixins import CreatesMetadataModelMixin
from edc_visit_tracking.constants import (
    UNSCHEDULED, SCHEDULED, COMPLETED_PROTOCOL_VISIT, MISSED_VISIT)
from edc_visit_tracking.model_mixins import CaretakerFieldsMixin, VisitModelMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_visit_tracking.managers import VisitModelManager

from td.models import Appointment

from .infant_birth import InfantBirth


class InfantVisitManager(VisitModelManager, models.Manager):

    def get_by_natural_key(self, subject_identifier, visit_code):
        return self.get(subject_identifier=subject_identifier, visit_code=visit_code)


class InfantVisit(
        VisitModelMixin, CreatesMetadataModelMixin, OffstudyMixin,
        CaretakerFieldsMixin, ExportTrackingFieldsMixin, UrlMixin, BaseUuidModel):

    """ A model completed by the user on the infant visits. """

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    objects = InfantVisitManager()

    history = HistoricalRecords()

    def natural_key(self):
        return super(InfantVisit, self).natural_key()
    natural_key.dependencies = ['td.appointment']

    def custom_post_update_crf_meta_data(self):
        """Calls custom methods that manipulate meta data on the post save.

        This method is called in a post-save signal in edc_meta_data."""
        if self.survival_status == DEAD:
            self.require_death_report()
        elif self.reason == COMPLETED_PROTOCOL_VISIT:
            self.require_off_study_report()
        elif self.reason == UNSCHEDULED:
            self.change_to_unscheduled_visit(self.appointment)
        elif self.reason == SCHEDULED:
            pass
        return self

    def requires_circumcision_for_male_at_2030_or_2060(self):
        infant_birth = InfantBirth.objects.get(
            registered_subject=self.appointment.registered_subject)
        if infant_birth.gender == MALE:
            if self.appointment.visit_code == '2030':
                self.crf_is_required(
                    self.appointment, 'td_infant', 'infantcircumcision')
            if self.appointment.visit_code == '2060':
                appointment = Appointment.objects.get(
                    visit_code='2030',
                    registered_subject=self.appointment.registered_subject)
                if appointment:
                    infant_visit = InfantVisit.objects.get(appointment=appointment)
                    if infant_visit.reason == MISSED_VISIT:
                        self.crf_is_required(
                            self.appointment, 'td_infant', 'infantcircumcision')

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Visit"
        verbose_name_plural = "Infant Visit"
