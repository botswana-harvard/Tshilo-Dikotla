from django.db import models
from django.apps import apps

from edc_base.model.validators import date_not_before_study_start, date_not_future
from edc_constants.choices import POS_NEG_UNTESTED_REFUSAL, YES_NO_NA, POS_NEG, YES_NO
from edc_constants.constants import NO
from edc_registration.models import RegisteredSubject

from .enrollment_helper import EnrollmentHelper


class EnrollmentMixin(models.Model):

    """Base Model for antenal and postnatal enrollment"""

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

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

    is_diabetic = models.CharField(
        verbose_name='Are you diabetic?',
        choices=YES_NO,
        help_text='INELIGIBLE if YES',
        max_length=3)

    will_breastfeed = models.CharField(
        verbose_name='Are you willing to breast-feed your child for 6 months?',
        choices=YES_NO,
        # default=NO,
        help_text='INELIGIBLE if NO',
        max_length=3)

    will_remain_onstudy = models.CharField(
        verbose_name="Are you willing to remain in the study for the child's first three year of life",
        choices=YES_NO,
        # default=NO,
        help_text='INELIGIBLE if NO',
        max_length=3)

    week32_test = models.CharField(
        verbose_name="Have you tested for HIV on OR after 32 weeks gestational age?",
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
        # default=NOT_APPLICABLE,
        choices=YES_NO_NA,
        help_text=("evidence = clinic and/or IDCC records. check regimes/drugs. If NO, participant"
                   "will not be enrolled"))

    valid_regimen = models.CharField(
        verbose_name="(Interviewer) If HIV +VE, do records show that participant takes ARV'\s?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        # default=NOT_APPLICABLE,
        max_length=15,
        help_text=("Valid regimes include: Atripla, Truvada-Efavirenz or Tenofovir, "
                   "Entricitibine-Efavirenz, Truvad-Lamivudine-Efavirenz. If NO, participant"
                   "will not be enrolled"))

    valid_regimen_duration = models.CharField(
        verbose_name="Has the participant been on the regimen for a valid period of time?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        # default=NOT_APPLICABLE,
        max_length=15,
        help_text=("If not 4 or more weeks then not eligible."))

    rapid_test_done = models.CharField(
        verbose_name="Was a rapid test processed?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        # default=NOT_APPLICABLE,
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

    def __unicode__(self):
        return "{0} {1}".format(
            self.registered_subject.subject_identifier,
            self.registered_subject.first_name)

    def save(self, *args, **kwargs):
        MaternalUltraSoundInitial = apps.get_model('td_maternal', 'MaternalUltraSoundInitial')
        try:
            maternal_ultrasound = MaternalUltraSoundInitial.objects.get(
                maternal_visit__appointment__registered_subject=self.registered_subject)
            enrollment_helper = EnrollmentHelper(instance_antenatal=self, instance_ultrasound=maternal_ultrasound)
        except MaternalUltraSoundInitial.DoesNotExist:
            enrollment_helper = EnrollmentHelper(instance_antenatal=self)
        self.is_eligible = enrollment_helper.is_eligible
        self.enrollment_hiv_status = enrollment_helper.enrollment_hiv_status
        self.date_at_32wks = enrollment_helper.date_at_32wks
        self.is_eligible, unenrolled_error_message = self.unenrolled_error_messages()
        self.unenrolled = unenrolled_error_message
        super(EnrollmentMixin, self).save(*args, **kwargs)

    def common_fields(self):
        """Returns a list of field names common to postnatal
        and antenatal enrollment models."""
        common_fields = []
        excluded_fields = ['is_eligible', 'enrollment_hiv_status', 'date_at_32wks', 'unenrolled']
        for field in EnrollmentMixin._meta.fields:
            if field.name not in excluded_fields:
                common_fields.append(field.name)
        return common_fields

    def get_registration_datetime(self):
        return self.report_datetime

    @property
    def subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    class Meta:
        abstract = True
