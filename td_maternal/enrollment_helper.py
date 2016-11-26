from dateutil.relativedelta import relativedelta

from django.apps import apps as django_apps

from edc_constants.constants import NO, YES, POS, NEG


class EnrollmentError(Exception):
    pass


class EnrollmentHelper(object):

    """Class that determines maternal eligibility based on the protocol specific criteria.

    * Accepts an instance of AntenatalEnrollment or PostnatalEnrollment.
    * is called in the save method of the EnrollmentMixin.
    * makes available the calculated enrollment_hiv_status and date_at_32wks
      which can be saved to the model instance.

    Note: it's assumed the form validates values to avoid raising an EnrollmentError here.

    For example:

        def save(self, *args, **kwargs):
            enrollment_helper = EnrollmentHelper(self)
            self.is_eligible = enrollment_helper.is_eligible
            self.enrollment_hiv_status = enrollment_helper.enrollment_hiv_status
            self.date_at_32wks = enrollment_helper.date_at_32wks
            super(EnrollmentMixin, self).save(*args, **kwargs)
    """

    def __init__(self, instance, exception_cls=None):
        self._ultrasound = None
        self._delivery = None
        self.instance = instance
        self.date_at_32wks = self.edd_by_lmp - relativedelta(weeks=6) if self.edd_by_lmp else None
        self.exception_cls = exception_cls or EnrollmentError

    @property
    def ga_lmp_enrollment_wks(self):
        return (int(40 - ((self.edd_by_lmp - self.instance.report_datetime.date()).days / 7)) if
                self.instance.last_period_date else None)

    @property
    def is_eligible(self):
        """Returns True if basic criteria is met for enrollment.

        Potentially required model instances:
            MaternalLabourDel
            MaternalUltraSoundInitial
        """
        is_eligible = False
        if self.pending_ultrasound or not self.ultrasound:
            meets_basic_criteria = False
        else:
            meets_basic_criteria = (
                self.lmp_to_use >= 16 and self.lmp_to_use <= 36 and
                self.no_chronic_conditions and self.instance.will_breastfeed == YES and
                self.instance.will_remain_onstudy == YES and self.pass_antenatal_enrollment and
                self.keep_on_study)
        if meets_basic_criteria and self.enrollment_hiv_status == POS and self.instance.will_get_arvs == YES:
            is_eligible = True
        elif meets_basic_criteria and self.enrollment_hiv_status == NEG:
            is_eligible = True
        else:
            is_eligible = False
        return is_eligible

    @property
    def keep_on_study(self):
        try:
            keep_on_study = self.delivery.keep_on_study
        except AttributeError:
            keep_on_study = True
        return keep_on_study

    @property
    def pass_antenatal_enrollment(self):
        try:
            pass_antenatal_enrollment = self.ultrasound.pass_antenatal_enrollment
        except AttributeError:
            pass_antenatal_enrollment = True
        return pass_antenatal_enrollment

    @property
    def lmp_to_use(self):
        return self.ga_lmp_enrollment_wks if self.ga_lmp_enrollment_wks else self.ultrasound.ga_confirmed

    @property
    def enrollment_hiv_status(self):
        """Returns the maternal HIV status at enrollment based on valid combinations
        expected from the form otherwise raises a EnrollmentError. Can only return POS or NEG.

        Note: the EnrollmentError should never be excepted!!"""
        pos = self.known_hiv_pos_with_evidence or self.tested_pos_at32wks or self.tested_pos_rapidtest
        neg = (self.tested_neg_at32wks or self.tested_neg_rapidtest or
               self.tested_neg_previously_result_within_3_months)
        if neg and not pos:
            return NEG
        elif pos and not neg:
            return POS
        else:
            # Case neg and pos OR not neg and not pos
            raise self.exception_cls(
                'Unable to determine maternal hiv status at enrollment. '
                'Got current_hiv_status={}, evidence_hiv_status={}, '
                'rapid_test_done={}, rapid_test_result={}'.format(
                    self.instance.current_hiv_status,
                    self.instance.evidence_hiv_status,
                    self.instance.rapid_test_done,
                    self.instance.rapid_test_result))

    @property
    def known_hiv_pos_with_evidence(self):
        """"""
        if self.instance.current_hiv_status == POS and self.instance.evidence_hiv_status == YES:
            return True
        return False

    @property
    def tested_pos_at32wks(self):
        if (self.instance.week32_test == YES and self.instance.week32_result == POS and
                self.instance.evidence_32wk_hiv_status == YES):
            return True
        return False

    @property
    def tested_pos_rapidtest(self):
        if self.instance.rapid_test_done == YES and self.instance.rapid_test_result == POS:
            return True
        return False

    @property
    def tested_neg_at32wks(self):
        """"""
        if (self.instance.week32_test == YES and self.test_date_is_on_or_after_32wks and
                self.instance.week32_result == NEG and
                self.instance.evidence_32wk_hiv_status == YES):
            return True
        return False

    @property
    def tested_neg_rapidtest(self):
        if self.instance.rapid_test_done == YES and self.instance.rapid_test_result == NEG:
            return True
        return False

    @property
    def tested_neg_previously_result_within_3_months(self):
        """Returns true if the 32 week test date is within 3months else false"""
        if (self.instance.week32_test == YES and self.instance.week32_result == NEG and
           self.instance.week32_test_date >
           (self.instance.report_datetime.date() - relativedelta(months=3))):
            return True
        return False

    @property
    def test_date_is_on_or_after_32wks(self):
        """Returns True if the test date is on or after 32 weeks gestational age."""
        if self.instance.rapid_test_date:
            if self.instance.week32_test_date > self.instance.rapid_test_date:
                raise self.exception_cls('Rapid test date cannot precede test date on or after 32 weeks')
        return (self.instance.week32_test_date >= self.date_at_32wks if self.date_at_32wks else None)

    @property
    def validate_rapid_test(self):
        """Returns True to indicate that a rapid test is not required, False to indicate a rapid test is required."""
        if self.known_hiv_pos_with_evidence or self.tested_pos_at32wks or self.tested_neg_at32wks:
            return True
        return False

    @property
    def raise_validation_error_for_rapidtest(self):
        if (not self.validate_rapid_test and self.instance.rapid_test_done != YES and
                self.instance.rapid_test_result not in [POS, NEG] and
                not self.tested_neg_previously_result_within_3_months):
                    raise self.exception_cls('A rapid test with a valid result of either POS or NEG is required. Ensure'
                                             ' this is the case.')

    @property
    def delivery(self):
        if self._delivery is None:
            try:
                MaternalLabourDel = django_apps.get_model('td_maternal', 'MaternalLabourDel')
                self._delivery = MaternalLabourDel.objects.get(
                    registered_subject__subject_identifier=self.instance.subject_identifier)
            except MaternalLabourDel.DoesNotExist:
                self._delivery = False
        return self._delivery

    @property
    def ultrasound(self):
        """Returns an MaternalUltrasoundInitial instance or None."""
        if self._ultrasound is None:
            try:
                MaternalUltrasoundInitial = django_apps.get_model('td_maternal', 'MaternalUltraSoundInitial')
                self._ultrasound = MaternalUltrasoundInitial.objects.get(
                    maternal_visit__appointment__subject_identifier=self.instance.subject_identifier)
            except MaternalUltrasoundInitial.DoesNotExist:
                self._ultrasound = False
        return self._ultrasound

    @property
    def pending_ultrasound(self):
        """Return True is subject does not have a ultrasound (instance) and lmp is not known."""
        pending_ultrasound = False
        try:
            if (not self.instance.ultrasound) and (NO in self.instance.knows_lmp):
                pending_ultrasound = True
        except AttributeError:
            pass
        return pending_ultrasound

    @property
    def edd_by_lmp(self):
        return (self.instance.last_period_date + relativedelta(days=280) if
                self.instance.last_period_date else None)

    @property
    def no_chronic_conditions(self):
        """Returns True if subject has no chronic conditions."""
        return self.instance.is_diabetic == NO

    def unenrolled_reasons(self):
        """Returns a tuple (True, None) if mother is eligible."""
        reasons = []
        if not self.is_eligible:
            reasons = ['Diabetic'] if self.instance.is_diabetic == YES else []
            if self.instance.will_breastfeed == NO:
                reasons.append('will not breastfeed')
            if self.instance.will_remain_onstudy == NO:
                reasons.append('won\'t remain in study')
            if self.instance.will_get_arvs == NO:
                reasons.append('Will not get ARVs on this pregnancy.')
            if self.instance.rapid_test_done == NO:
                reasons.append('rapid test not done')
            if self.ga_lmp_enrollment_wks and (self.ga_lmp_enrollment_wks < 16 or self.ga_lmp_enrollment_wks > 36):
                reasons.append('gestation not 16 to 36wks')
            if self.delivery and not self.keep_on_study:
                reasons.append('Hiv+ and not on ART for atleast 4 weeks.')
            if self.ultrasound and not self.pass_antenatal_enrollment:
                reasons.append('Pregnancy is not a singleton.')
        return reasons
