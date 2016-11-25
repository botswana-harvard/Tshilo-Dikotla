from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_export.model_mixins import ExportTrackingFieldsMixin
from edc_offstudy.model_mixins import OffstudyModelMixin


class MaternalOffStudy(OffstudyModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    """ A model completed by the user on the visit when the mother is taken off-study. """

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Off Study"
        consent_model = 'td_maternal.maternalconsent'
        visit_schedule_name = 'maternal_visit_schedule.maternal_enrollment_step1'
