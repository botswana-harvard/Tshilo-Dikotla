from edc_constants.constants import NO, YES, UNKNOWN, POS, NEG, IND, NOT_APPLICABLE, SEROCONVERSION, NEVER, DWTA
from dateutil.relativedelta import relativedelta
from tshilo_dikotla.apps.td.constants import LIVE


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
            enrollment_helper = EnrollmentHelper(instance=self)
            self.is_eligible = enrollment_helper.is_eligible
            self.enrollment_hiv_status = enrollment_helper.enrollment_hiv_status
            self.date_at_32wks = enrollment_helper.date_at_32wks
            super(EnrollmentMixin, self).save(*args, **kwargs)
    """

    def __init__(self, instance, exception_cls=None):
        self._enrollment_hiv_status = None
        self.date_at_32wks = None
        self.instance = instance
        self.enrollment = self.instance._meta.verbose_name
        self.exception_cls = exception_cls or EnrollmentError

        # make all fields from the enrollment instance available to this instance
        for field in self.instance._meta.fields:
            try:
                setattr(self, field.name, getattr(self.instance, field.name))
            except AttributeError:
                pass

        self.is_eligible = self.is_eligible_for_enrollment()

    def is_eligible_for_enrollment(self):
        """Returns True if all eligibility criteria passes."""
        is_eligible = False
        if self.antenatal_criteria():
            if (self.enrollment_hiv_status == POS and self.valid_regimen == YES and
                    self.valid_regimen_duration == YES):
                is_eligible = True
            elif self.enrollment_hiv_status == NEG:
                is_eligible = True
        return is_eligible

    def antenatal_criteria(self):
        """Returns True if basic criteria, not including HIV status,
        is met for antenatal enrollment."""
        if (self.gestation_wks >= 16 and self.gestation_wks <= 36 and self.no_chronic_conditions() and
                self.will_breastfeed == YES and self.will_remain_onstudy == YES and self.no_chronic_conditions()):
            return True
        return False

    @property
    def enrollment_hiv_status(self):
        """Returns the maternal HIV status at enrollment based on valid combinations
        expected from the form otherwise raises a EnrollmentError.

        Note: the EnrollmentError should never be excepted!!"""
        if not self._enrollment_hiv_status:
            if self.evidence_hiv_status == YES:
                self._enrollment_hiv_status = self.hiv_status_with_evidence()
            elif self.evidence_hiv_status in [NO, NOT_APPLICABLE]:
                self._enrollment_hiv_status = self.hiv_status_with_without_evidence()
            if not self._enrollment_hiv_status:
                raise self.exception_cls(
                    'Unable to determine maternal hiv status at enrollment. '
                    'Got current_hiv_status={}, evidence_hiv_status={}, '
                    'rapid_test_done={}, rapid_test_result={}'.format(
                        self.current_hiv_status,
                        self.evidence_hiv_status,
                        self.rapid_test_done,
                        self.rapid_test_result))
        return self._enrollment_hiv_status

    def hiv_status_with_evidence(self):
        """Returns the hiv status if evidence is available or None."""
        hiv_status = None
        if self.evidence_hiv_status == YES:
            if self.hiv_status_on_or_after_32wk(self.exception_cls) == POS:
                hiv_status = POS
            elif self.hiv_status_on_or_after_32wk(self.exception_cls) == NEG:
                hiv_status = NEG
            elif self.current_hiv_status == POS and self.rapid_test_done in [NO, NOT_APPLICABLE]:
                hiv_status = POS
            elif self.current_hiv_status == NEG and self.rapid_test_done in [NO, NOT_APPLICABLE]:
                hiv_status = UNKNOWN
            elif (self.current_hiv_status == POS and self.rapid_test_done == YES and
                    self.rapid_test_result == POS):
                hiv_status = POS
            elif (self.current_hiv_status == NEG and
                    self.rapid_test_done == YES and self.rapid_test_result == NEG):
                hiv_status = NEG
            elif (self.current_hiv_status == NEG and
                    self.rapid_test_done == YES and self.rapid_test_result == POS):
                hiv_status = SEROCONVERSION
            elif (self.current_hiv_status == NEG and
                    self.rapid_test_done == YES and self.rapid_test_result == IND):
                hiv_status = IND
        return hiv_status

    def hiv_status_with_without_evidence(self):
        """Returns the hiv status if evidence is not available or None."""
        if self.evidence_hiv_status in [NO, NOT_APPLICABLE]:
            if (self.current_hiv_status == POS and self.rapid_test_done == YES and
                    self.rapid_test_result == POS):
                hiv_status = POS
            elif (self.current_hiv_status == POS and self.rapid_test_done == NO and
                    self.rapid_test_result is None):
                hiv_status = UNKNOWN
            elif (self.current_hiv_status in [NEG, NEVER, UNKNOWN, DWTA] and self.rapid_test_done == YES and
                    self.rapid_test_result == NEG):
                hiv_status = NEG
            elif (self.current_hiv_status in [NEG, NEVER, UNKNOWN, DWTA] and self.rapid_test_done == YES and
                    self.rapid_test_result == POS):
                hiv_status = SEROCONVERSION
            elif (self.current_hiv_status in [NEG, NEVER, UNKNOWN, DWTA] and self.rapid_test_done == NO and
                    self.rapid_test_result is None):
                hiv_status = UNKNOWN
        return hiv_status

    def hiv_status_on_or_after_32wk(self, exception_cls=None):
        """Returns the maternal status on or after week 32 gestational age or None."""
        hiv_status = None
        exception_cls = exception_cls or EnrollmentError
        if self.week32_test == YES and self.week32_test_date:
            if not self.test_date_is_on_or_after_32wks():
                raise exception_cls(
                    'Test date is not on or after 32 weeks gestational age.')
            elif self.week32_result == POS and self.current_hiv_status == POS:
                hiv_status = POS
            elif self.week32_result == NEG and self.current_hiv_status == NEG:
                hiv_status = NEG
        return hiv_status

    def test_date_is_on_or_after_32wks(self):
        """Returns True if the test date is on or after 32 weeks gestational age."""
        self.date_at_32wks = self.report_datetime.date() - relativedelta(weeks=self.gestational_age - 32)
        if self.rapid_test_date:
            if self.week32_test_date > self.rapid_test_date:
                raise self.exception_cls('Rapid test date cannot precede test date on or after 32 weeks')
        return self.week32_test_date >= self.date_at_32wks

    def no_chronic_conditions(self):
        """Returns True if subject has no chronic conditions."""
        return (self.is_diabetic == NO)
