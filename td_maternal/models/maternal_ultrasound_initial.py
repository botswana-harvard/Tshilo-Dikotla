from django.db import models

from edc_pregnancy_utils import Edd, Lmp, Ultrasound, Ga
from edc_protocol.validators import date_not_before_study_start

from td.choices import GESTATIONS_NUMBER
from td.validators import validate_ga_by_ultrasound, validate_fetal_weight

from ..choices import CONFIRMATION_METHOD

from .base_ultra_sound_model import BaseUtraSoundModel
from td_maternal.models.antenatal_enrollment import AntenatalEnrollment


class MaternalUltraSoundInitial(BaseUtraSoundModel):

    """ The initial ultra sound model that influences mother's enrollment in to study. """

    ADMIN_SITE_NAME = 'td_maternal_admin'

    number_of_gestations = models.CharField(
        verbose_name="Number of viable gestations seen?",
        max_length=3,
        choices=GESTATIONS_NUMBER,
        help_text='If number is not equal to 1, then participant goes off study.')

    ga_by_lmp = models.IntegerField(
        verbose_name="GA by LMP at ultrasound date",
        null=True,
        blank=True,
        help_text='Units in weeks. Derived variable, see AntenatalEnrollment.')

    ga_by_ultrasound_wks = models.IntegerField(
        verbose_name="GA by ultrasound in weeks",
        validators=[validate_ga_by_ultrasound, ],
        help_text='Units in weeks.')

    ga_by_ultrasound_days = models.IntegerField(
        verbose_name="GA by ultrasound days offset",
        help_text='must be less than 7days.')

    est_fetal_weight = models.DecimalField(
        verbose_name="Estimated fetal weight",
        validators=[validate_fetal_weight, ],
        max_digits=8,
        decimal_places=2,
        help_text='Units in grams.')

    est_edd_ultrasound = models.DateField(
        verbose_name="Estimated date of delivery by ultrasound",
        validators=[
            date_not_before_study_start],
        help_text='EDD')

    edd_confirmed = models.DateField(
        verbose_name="EDD Confirmed.",
        null=True,
        editable=False,
        help_text='Derived variable.')

    edd_method = models.CharField(
        verbose_name="The method used to derive edd.",
        max_length=3,
        choices=CONFIRMATION_METHOD,
        null=True,
        editable=False,
        help_text='Derived variable.')

    ga_confirmed = models.IntegerField(
        verbose_name="GA confirmed in weeks.",
        null=True,
        editable=False,
        help_text='Derived variable.')

    ga_method = models.CharField(
        verbose_name="The method used to derive ga.",
        max_length=3,
        choices=CONFIRMATION_METHOD,
        null=True,
        editable=False,
        help_text='Derived variable.')

    def save(self, *args, **kwargs):
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        self.ga_by_lmp = antenatal_enrollment.ga_lmp_enrollment_wks
        lmp = Lmp(
            lmp=antenatal_enrollment.last_period_date,
            reference_date=self.report_datetime.date())
        ultrasound = Ultrasound(
            ultrasound_date=self.report_datetime.date(),
            ga_confirmed_weeks=self.ga_by_ultrasound_wks,
            ga_confirmed_days=self.ga_by_ultrasound_days,
            ultrasound_edd=self.est_edd_ultrasound)
        try:
            self.est_edd_ultrasound = self.est_edd_ultrasound.date()
        except AttributeError:
            pass
        ga = Ga(lmp, ultrasound, prefer_ultrasound=True)
        edd = Edd(lmp=lmp, ultrasound=ultrasound)
        self.ga_confirmed = ga.weeks
        self.ga_method = str(ga.method)
        self.edd_confirmed = edd.edd
        self.edd_method = str(edd.method)
        super(MaternalUltraSoundInitial, self).save(*args, **kwargs)

    class Meta(BaseUtraSoundModel.Meta):
        app_label = 'td_maternal'
        verbose_name = "Maternal Ultra Sound Initial"
