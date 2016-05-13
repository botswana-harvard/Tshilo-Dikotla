from django.db import models
from django.apps import apps

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future)
from edc_consent.models import RequiresConsentMixin
from edc_export.models import ExportTrackingFieldsMixin
from edc_meta_data.managers import CrfMetaDataManager
from edc_offstudy.models import OffStudyModelMixin
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfModelMixin

from tshilo_dikotla.apps.td.choices import MALFORMATIONS
from .maternal_crf_model import MaternalCrfModel


class BaseUtraSoundModel(MaternalCrfModel):

    """ The base ultra sound model. """

    bpd = models.DecimalField(
        verbose_name="BDP?",
        max_digits=6,
        decimal_places=2,
        help_text='Units in mm.')

    hc = models.DecimalField(
        verbose_name="HC?",
        max_digits=6,
        decimal_places=2,
        help_text='Units in mm.')

    ac = models.DecimalField(
        verbose_name="AC?",
        max_digits=6,
        decimal_places=2,
        help_text='Units in mm.')

    fl = models.DecimalField(
        verbose_name="FL?",
        max_digits=6,
        decimal_places=2,
        help_text='Units in mm.')

    hl = models.DecimalField(
        verbose_name="HL?",
        max_digits=6,
        decimal_places=2,
        help_text='Units in mm.')

    lateral_ventricle = models.DecimalField(
        verbose_name="Lateral Ventricle",
        max_digits=6,
        decimal_places=2,
        help_text='Units in mm.')

    cerebellum = models.DecimalField(
        verbose_name="Cerebellum?",
        max_digits=6,
        decimal_places=2,
        help_text='Units in mm.')

    cistema_magna = models.DecimalField(
        verbose_name="Cistema Magna",
        max_digits=6,
        decimal_places=2,
        help_text='Units in mm.')

    malformations = models.CharField(
        verbose_name="Amniotic fluid volume?",
        max_length=50,
        choices=MALFORMATIONS,
        help_text='')

    @property
    def antenatal_enrollment(self):
        AntenatalEnrollment = apps.get_model('td_maternal', 'antenatalenrollment')
        return AntenatalEnrollment.objects.get(registered_subject=self.maternal_visit.appointment.registered_subject)

    class Meta:
        abstract = True
