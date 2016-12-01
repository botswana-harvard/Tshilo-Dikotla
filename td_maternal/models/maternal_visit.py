from django.db import models

from edc_base.model.models import BaseUuidModel, UrlMixin, HistoricalRecords
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import CreatesMetadataModelMixin
from edc_visit_tracking.choices import VISIT_REASON
from edc_visit_tracking.model_mixins import (VisitModelMixin, CaretakerFieldsMixin)
from edc_visit_tracking.managers import VisitModelManager

from td.models import Appointment


class MaternalVisit(CreatesMetadataModelMixin, RequiresConsentMixin, CaretakerFieldsMixin,
                    VisitModelMixin, UrlMixin, BaseUuidModel):

    """ Maternal visit form that links all antenatal/ postnatal follow-up forms """

    appointment = models.OneToOneField(Appointment, on_delete=models.PROTECT)

    objects = VisitModelManager()

    history = HistoricalRecords()

    def natural_key(self):
        return super()

    def __str__(self):
        return '{} {} {}'.format(self.appointment.subject_identifier,
                                 self.antenatal_enrollment.registered_subject.first_name,
                                 self.appointment.visit_code)

    def save(self, *args, **kwargs):
        self.subject_identifier = self.appointment.subject_identifier
        super(MaternalVisit, self).save(*args, **kwargs)

    def get_visit_reason_choices(self):
        return VISIT_REASON

    @property
    def enrollment_hiv_status(self):
        enrollment_hiv_status = None
        try:
            enrollment_hiv_status = self.antenatal_enrollment.enrollment_hiv_status
        except AttributeError:
            pass
        return enrollment_hiv_status

    def get_subject_identifier(self):
        return self.appointment.subject_identifier

    class Meta(VisitModelMixin.Meta):
        app_label = 'td_maternal'
        verbose_name = 'Maternal Visit'
        consent_model = 'td_maternal.maternalconsent'
        visit_schedule_name = 'maternal_visit_schedule'
