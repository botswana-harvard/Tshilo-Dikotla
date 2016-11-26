from django.db import models
from django.apps import apps

from td.choices import AMNIOTIC_FLUID
from td.validators import validate_bpd, validate_hc, validate_fl, validate_ac

from .maternal_crf_model import MaternalCrfModel


class BaseUtraSoundModel(MaternalCrfModel):

    """ The base ultra sound model. """

    bpd = models.DecimalField(
        verbose_name="BPD?",
        validators=[validate_bpd, ],
        max_digits=6,
        decimal_places=2,
        help_text='Units in cm.')

    hc = models.DecimalField(
        verbose_name="HC?",
        validators=[validate_hc, ],
        max_digits=6,
        decimal_places=2,
        help_text='Units in cm.')

    ac = models.DecimalField(
        verbose_name="AC?",
        validators=[validate_ac, ],
        max_digits=6,
        decimal_places=2,
        help_text='Units in cm.')

    fl = models.DecimalField(
        verbose_name="FL?",
        validators=[validate_fl, ],
        max_digits=6,
        decimal_places=2,
        help_text='Units in cm.')

    amniotic_fluid_volume = models.CharField(
        verbose_name="Amniotic fluid volume?",
        max_length=10,
        choices=AMNIOTIC_FLUID,
        help_text='')

    @property
    def antenatal_enrollment(self):
        AntenatalEnrollment = apps.get_model('td_maternal', 'antenatalenrollment')
        return AntenatalEnrollment.objects.get(registered_subject__subject_identifier=self.maternal_visit.appointment.subject_identifier)

    class Meta(MaternalCrfModel.Meta):
        abstract = True
