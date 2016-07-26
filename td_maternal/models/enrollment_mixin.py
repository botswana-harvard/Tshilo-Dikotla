from django.db import models
from django.apps import apps
from django.core.exceptions import ValidationError

from edc_base.model.validators import (date_not_before_study_start, date_not_future,
                                       datetime_not_future, datetime_not_before_study_start)
from edc_constants.choices import POS_NEG_UNTESTED_REFUSAL, YES_NO_NA, POS_NEG, YES_NO
from edc_constants.constants import NO, YES, POS, NEG
from edc_registration.models import RegisteredSubject

from .enrollment_helper import EnrollmentHelper


class EnrollmentMixin(models.Model):

    """Base Model for antenal enrollment"""

    registered_subject = models.OneToOneField(RegisteredSubject)

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    enrollment_hiv_status = models.CharField(
        max_length=15,
        null=True,
        editable=False,
        help_text='Auto-filled by enrollment helper')

    date_at_32wks = models.DateField(
        null=True,
        editable=False,
        help_text='Auto-filled by enrollment helper')

    is_eligible = models.BooleanField(
        editable=False)

    pending_ultrasound = models.BooleanField(
        editable=False)

    is_diabetic = models.CharField(
        verbose_name='Are you diabetic?',
        choices=YES_NO,
        help_text='INELIGIBLE if YES',
        max_length=3)

    will_breastfeed = models.CharField(
        verbose_name='Are you willing to breast-feed your child for 6 months?',
        choices=YES_NO,
        help_text='INELIGIBLE if NO',
        max_length=3)

    will_remain_onstudy = models.CharField(
        verbose_name="Are you willing to remain in the study for the child's first three year of life",
        choices=YES_NO,
        help_text='INELIGIBLE if NO',
        max_length=3)

    current_hiv_status = models.CharField(
        verbose_name="What is your current HIV status?",
        choices=POS_NEG_UNTESTED_REFUSAL,
        max_length=30,
        help_text=("if POS or NEG, ask for documentation."))

    evidence_hiv_status = models.CharField(
        verbose_name="(Interviewer) Have you seen evidence of the HIV result?",
        max_length=15,
        null=True,
        blank=False,
        choices=YES_NO_NA,
        help_text=("evidence = clinic and/or IDCC records. check regimes/drugs. If NO, more criteria required."))

    week32_test = models.CharField(
        verbose_name="Have you tested for HIV before or during this pregnancy?",
        choices=YES_NO,
        default=NO,
        max_length=3)

    week32_test_date = models.DateField(
        verbose_name="Date of HIV Test",
        null=True,
        blank=True)

    week32_result = models.CharField(
        verbose_name="What was your result?",
        choices=POS_NEG,
        max_length=15,
        null=True,
        blank=True)

    evidence_32wk_hiv_status = models.CharField(
        verbose_name="(Interviewer) Have you seen evidence of the result from HIV test on or before this pregnancy?",
        max_length=15,
        null=True,
        blank=False,
        choices=YES_NO_NA,
        help_text=("evidence = clinic and/or IDCC records. check regimes/drugs."))

    will_get_arvs = models.CharField(
        verbose_name="(Interviewer) If HIV+ve, do records show that participant is taking, is prescribed,"
                     "or will be prescribed ARVs (if newly diagnosed) during pregnancy?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        max_length=15,
        help_text=("If found POS by RAPID TEST. Then answer YES, can take them OFF STUDY at birth visit if there were"
                   " not on therapy for atleast 4 weeks."))

    rapid_test_done = models.CharField(
        verbose_name="Was a rapid test processed?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        max_length=15,
        help_text=(
            'Remember, rapid test is for NEG, UNTESTED, UNKNOWN and Don\'t want to answer.'))

    rapid_test_date = models.DateField(
        verbose_name="Date of rapid test",
        null=True,
        validators=[
            date_not_before_study_start,
            date_not_future],
        blank=True)

    rapid_test_result = models.CharField(
        verbose_name="What is the rapid test result?",
        choices=POS_NEG,
        max_length=15,
        null=True,
        blank=True)

    unenrolled = models.TextField(
        verbose_name="Reason not enrolled",
        max_length=350,
        null=True,
        editable=False)

    def __str__(self):
        return "{0} {1}".format(
            self.registered_subject.subject_identifier,
            self.registered_subject.first_name)

    def save(self, *args, **kwargs):
        enrollment_helper = EnrollmentHelper(instance_antenatal=self)
#         if not enrollment_helper.validate_rapid_test():
#             raise ValidationError('Ensure a rapid test id done for this subject.')
        self.edd_by_lmp = enrollment_helper.evaluate_edd_by_lmp
        self.ga_lmp_enrollment_wks = enrollment_helper.evaluate_ga_lmp(self.report_datetime.date())
        self.enrollment_hiv_status = enrollment_helper.enrollment_hiv_status
        self.date_at_32wks = enrollment_helper.date_at_32wks
        if not self.ultrasound:
            self.pending_ultrasound = enrollment_helper.pending
        self.is_eligible = self.antenatal_criteria(enrollment_helper)
        self.unenrolled = self.unenrolled_error_messages()
        super(EnrollmentMixin, self).save(*args, **kwargs)

    def antenatal_criteria(self, enrollment_helper):
        """Returns True if basic criteria is met for enrollment."""
        if self.pending_ultrasound:
            basic_criteria = False
        else:
            lmp_to_use = self.ga_lmp_enrollment_wks if self.ga_lmp_enrollment_wks else self.ultrasound.ga_confirmed
            basic_criteria = (lmp_to_use >= 16 and lmp_to_use <= 36 and
                              enrollment_helper.no_chronic_conditions() and self.will_breastfeed == YES and
                              self.will_remain_onstudy == YES and
                              (self.ultrasound.pass_antenatal_enrollment if self.ultrasound else True) and
                              (self.delivery.keep_on_study if self.delivery else True))
        if basic_criteria and self.enrollment_hiv_status == POS and self.will_get_arvs == YES:
            return True
        elif basic_criteria and self.enrollment_hiv_status == NEG:
            return True
        else:
            return False

    def get_registration_datetime(self):
        return self.report_datetime

    @property
    def ultrasound(self):
        MaternalUltraSoundInitial = apps.get_model('td_maternal', 'MaternalUltraSoundInitial')
        try:
            return MaternalUltraSoundInitial.objects.get(
                maternal_visit__appointment__registered_subject=self.registered_subject)
        except MaternalUltraSoundInitial.DoesNotExist:
            return None

    @property
    def delivery(self):
        MaternalLabourDel = apps.get_model('td_maternal', 'MaternalLabourDel')
        try:
            return MaternalLabourDel.objects.get(
                registered_subject=self.registered_subject)
        except MaternalLabourDel.DoesNotExist:
            return None

    @property
    def subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    class Meta:
        abstract = True
