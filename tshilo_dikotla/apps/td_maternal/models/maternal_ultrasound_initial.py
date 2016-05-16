from django.db import models

from edc_base.model.validators import date_not_before_study_start, date_not_future

from tshilo_dikotla.apps.td.choices import GESTATIONS_NUMBER,  ZERO_ONE

from .antenatal_enrollment import AntenatalEnrollment
from .base_ultra_sound_model import BaseUtraSoundModel


class MaternalUltraSoundInitial(BaseUtraSoundModel):

    """ The initial ultra sound model that influences mother's enrollment in to study. """

    number_of_gestations = models.CharField(
        verbose_name="Number of viable gestations seen?",
        max_length=3,
        choices=GESTATIONS_NUMBER,
        help_text='If number is not equal to 1, then participant goes off study.')

    ga_by_lmp = models.IntegerField(
        verbose_name="GA by LMP at ultrasound date")

    ga_by_ultrasound_wks = models.IntegerField(
        verbose_name="GA by ultrasound in weeks",
        help_text='Units in weeks.')

    ga_by_ultrasound_days = models.IntegerField(
        verbose_name="GA by ultrasound days offset",
#         max_value=6,
        help_text='must be less than 7days.')

    est_fetal_weight = models.DecimalField(
        verbose_name="Estimated fetal weight",
        max_digits=8,
        decimal_places=2,
        help_text='Units in grams.')

    est_edd = models.DateField(
        verbose_name="Estimated date of delivery by ultrasound",
        validators=[
            date_not_before_study_start],
        help_text='EDD')

    edd_confirmed = models.DateField(
        verbose_name="EDD Confirmed.",
        help_text='EDD Confirmed. Derived variable.')

    ga_confirmed = models.IntegerField(
        verbose_name="GA confirmed from ultrasound date",
        help_text='must be less than 7days.')

    amniotic_fluid_volume = models.CharField(
        verbose_name="Amniotic fluid volume?",
        max_length=3,
        choices=ZERO_ONE,
        help_text='')

    ga_confrimation_method = models.CharField(
        verbose_name="The method used to derive edd_confirmed.",
        max_length=3,
        choices=ZERO_ONE,
        help_text='0=EDD Confirmed by edd_by_lmp, 1=EDD Confirmed by edd_by_ultrasound.')

    def save(self, *args, **kwargs):
        # What if values in AntenatalEnrollment change?
        # They cannot. Antenatal Enrollment cannot be updated once UltraSound form has gone in without DMC intervention.
        # This is because it can potentially affect enrollment eligibility.
        self.ga_by_lmp = self.evaluate_ga_by_lmp()
        self.edd_confirmed, self.ga_confrimation_method = self.evaluate_edd_confirmed()
        self.ga_confirmed = self.evaluate_ga_confirmed()
        super(MaternalUltraSoundInitial, self).save(*args, **kwargs)

    @property
    def pass_antenatal_enrollment(self):
        return True if int(self.number_of_gestations) == 1 else False

    def evaluate_ga_by_lmp(self):
        return int(abs(40 - ((self.antenatal_enrollment.edd_by_lmp - self.report_datetime.date()).days / 7)))

    def evaluate_edd_confirmed(self):
        edd_by_lmp = self.antenatal_enrollment.edd_by_lmp
        if self.ga_by_lmp > 16 and self.ga_by_lmp < 22:
            if (edd_by_lmp - self.est_edd).days > 10:
                return (self.est_edd, 1)
        elif self.ga_by_lmp > 22 and self.ga_by_lmp < 28:
            if (edd_by_lmp - self.est_edd).days > 14:
                return (self.est_edd, 1)
        elif self.ga_by_lmp > 28:
            if (edd_by_lmp - self.est_edd).days > 21:
                return (self.est_edd, 1)
        else:
            return (edd_by_lmp, 0)

    def evaluate_ga_confirmed(self):
        return int(abs(40 - ((self.edd_confirmed - self.report_datetime.date()).days / 7)))

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Ultra Sound Initial"
