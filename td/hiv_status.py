from dateutil.relativedelta import relativedelta

from edc_constants.constants import YES, POS, NEG


class EnrollmentStatusError(Exception):
    pass


class Week32Error(Exception):
    pass


class EnrollmentStatus:
    """Determines hiv status for enrollment, returns POS, NEG or None.

    Raises an exception if a rapid test is required."""
    def __init__(self, obj, exception_cls=None):
        self.result = None
        self.exception_cls = exception_cls or EnrollmentStatusError
        self.current = Current(obj)
        self.rapid = Rapid(obj)
        self.week32 = Week32(obj)
        try:
            if self.week32.date > self.rapid.date:
                raise self.exception_cls('Rapid test date cannot precede test date on or after 32 weeks')
        except TypeError:
            pass
        if self.current.result == POS or self.week32.result == POS or self.rapid.result == POS:
            self.result = POS
        elif self.rapid.result == NEG or self.week32.result == NEG:
            self.result = NEG
        if self.current.result != POS and self.week32.result != POS:
            if not self.rapid.result:
                raise self.exception_cls(
                    'A rapid test result is required. Got current.result == {}, week32.result == {}'.format(
                        self.current.result, self.week32.result))


class Current:
    """Current HIV result/status, but only if POS, returns POS or None"""
    def __init__(self, obj):
        self.result = None
        if obj.evidence_hiv_status == YES and obj.current_hiv_status == POS:
            self.result = POS


class Week32:
    """HIV result by test at week 32, returns POS, NEG or None.

    within_3m is not inclusive."""
    def __init__(self, obj):
        self.result = None
        self.tested = obj.week32_test
        try:
            self.date = obj.week32_test_date.date()
        except AttributeError:
            self.date = obj.week32_test_date
        if obj.week32_test == YES:
            try:
                self.within_3m = self.date > (obj.report_datetime - relativedelta(months=3)).date()
            except TypeError:
                raise Week32Error('Invalid dates for within_3m calc.')
            if obj.week32_result == POS and obj.evidence_32wk_hiv_status == YES:
                self.result = POS
            elif obj.week32_result == NEG and obj.evidence_32wk_hiv_status == YES and self.within_3m:
                self.result = NEG


class Rapid:
    """HIV result by rapid test if cannot determine POS status by other means."""
    def __init__(self, obj):
        self.result = None
        self.date = None
        self.tested = obj.rapid_test_done
        if self.tested == YES:
            self.result = obj.rapid_test_result
            try:
                self.date = obj.rapid_test_date.date()
            except AttributeError:
                self.date = obj.rapid_test_date
