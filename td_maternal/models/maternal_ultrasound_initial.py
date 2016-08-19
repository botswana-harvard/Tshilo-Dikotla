from django.db import models
from django.core.exceptions import ValidationError

from edc_base.model.validators import date_not_before_study_start

from tshilo_dikotla.choices import GESTATIONS_NUMBER, ZERO_ONE
from tshilo_dikotla.validators import validate_ga_by_ultrasound, validate_fetal_weight

from .base_ultra_sound_model import BaseUtraSoundModel


class MaternalUltraSoundInitial(BaseUtraSoundModel):

    """ The initial ultra sound model that influences mother's enrollment in to study. """

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
        help_text='EDD Confirmed. Derived variable, see AntenatalEnrollment.')

    ga_confirmed = models.IntegerField(
        verbose_name="GA confirmed.",
        help_text='Derived variable.')

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
        return (int(abs(40 - ((self.antenatal_enrollment.edd_by_lmp - self.report_datetime.date()).days / 7))) if
                self.antenatal_enrollment.edd_by_lmp else None)

    def evaluate_edd_confirmed(self, error_clss=None):
        ga_by_lmp = self.evaluate_ga_by_lmp()
        edd_by_lmp = self.antenatal_enrollment.edd_by_lmp
        if not edd_by_lmp:
            return (self.est_edd_ultrasound, 1)
        error_clss = error_clss or ValidationError
        if ga_by_lmp > 16 and ga_by_lmp < 22:
            if abs((edd_by_lmp - self.est_edd_ultrasound).days) > 10:
                return (self.est_edd_ultrasound, 1)
            else:
                return (edd_by_lmp, 0)
#             raise error_clss('Unable to correctly determine edd_confirmed. ga_by_lmp=\'{}\', edd_by_lmp=\'{}\''
#                              ' est_edd_ultrasound=\'{}\''.format(ga_by_lmp, edd_by_lmp, self.est_edd_ultrasound))
        elif ga_by_lmp > 22 and ga_by_lmp < 28:
            if abs((edd_by_lmp - self.est_edd_ultrasound).days) > 14:
                return (self.est_edd_ultrasound, 1)
            else:
                return (edd_by_lmp, 0)
#             raise error_clss('Unable to correctly determine edd_confirmed. ga_by_lmp=\'{}\', edd_by_lmp=\'{}\''
#                              ' est_edd_ultrasound=\'{}\''.format(ga_by_lmp, edd_by_lmp, self.est_edd_ultrasound))
        elif ga_by_lmp > 28:
            if abs((edd_by_lmp - self.est_edd_ultrasound).days) > 21:
                return (self.est_edd_ultrasound, 1)
            else:
                return (edd_by_lmp, 0)
#             raise error_clss('Unable to correctly determine edd_confirmed. ga_by_lmp=\'{}\', edd_by_lmp=\'{}\''
#                              ' est_edd_ultrasound=\'{}\''.format(ga_by_lmp, edd_by_lmp, self.est_edd_ultrasound))
        else:
            return (edd_by_lmp, 0)

    def evaluate_ga_confirmed(self):
        return int(abs(40 - ((self.edd_confirmed - self.report_datetime.date()).days / 7)))

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Ultra Sound Initial"
