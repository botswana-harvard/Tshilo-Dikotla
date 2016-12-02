from django.db import models

from edc_base.model.models import BaseUuidModel, UrlMixin, HistoricalRecords
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import CreatesMetadataModelMixin
from edc_visit_tracking.model_mixins import (VisitModelMixin, CaretakerFieldsMixin)
from edc_visit_tracking.managers import VisitModelManager

from td.models import Appointment


class MaternalVisit(VisitModelMixin, CreatesMetadataModelMixin, RequiresConsentMixin, CaretakerFieldsMixin,
                    UrlMixin, BaseUuidModel):

    """ Maternal visit form that links all antenatal/ postnatal follow-up forms """

    appointment = models.OneToOneField(Appointment, on_delete=models.PROTECT)

    objects = VisitModelManager()

    history = HistoricalRecords()

    def natural_key(self):
        return super(MaternalVisit, self).natural_key()
    natural_key.dependencies = ['td.appointment']

    def __str__(self):
        return '{} {} {}'.format(
            self.subject_identifier,
            self.antenatal_enrollment.registered_subject.first_name,
            self.visit_code)

    def save(self, *args, **kwargs):
        self.subject_identifier = self.appointment.subject_identifier
        super(MaternalVisit, self).save(*args, **kwargs)

    class Meta(VisitModelMixin.Meta):
        app_label = 'td_maternal'
        verbose_name = 'Maternal Visit'
        consent_model = 'td_maternal.maternalconsent'
