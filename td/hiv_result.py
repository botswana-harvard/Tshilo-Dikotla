from dateutil.relativedelta import relativedelta

from edc_constants.constants import YES, POS, NEG


class EnrollmentResultError(Exception):
    pass


class EnrollmentNoResultError(Exception):
    pass


class EnrollmentRapidTestRequiredError(Exception):
    pass


class RecentResultError(Exception):
    pass


class Enrollment:
    """Determines hiv status for enrollment, returns POS, NEG or None.

    Raises an exception if a rapid test is required."""
    def __init__(self, current=None, recent=None, rapid=None, exception_cls=None):
        self.result = None
        self.exception_cls = exception_cls or EnrollmentResultError
        self.current = current
        self.recent = recent
        self.rapid = rapid
        try:
            if self.recent.date > self.rapid.date:
                raise self.exception_cls('Rapid test date cannot precede test date on or after 32 weeks')
        except TypeError:
            pass
        if self.current.result == POS or self.recent.result == POS or self.rapid.result == POS:
            self.result = POS
        elif self.rapid.result == NEG or self.recent.result == NEG:
            self.result = NEG
        if self.current.result != POS and self.recent.result != POS:
            if not self.rapid.result:
                raise self.exception_cls(
                    'A rapid test result is required. Got current.result == {}, recent.result == {}'.format(
                        self.current.result, self.recent.result))
        if self.result not in [POS, NEG]:
            if self.rapid.result:
                raise EnrollmentNoResultError('Unable to determine a POS or NEG result. Got {}.'.format(self.result))
            else:
                raise EnrollmentRapidTestRequiredError('Rapid test is required.')


class Test:
    """"""
    def __init__(self, tested=None, result=None, result_date=None):
        self.date = None
        self.result = None
        if tested == YES and result_date and result:
            self.result = result
            try:
                self.date = result_date.date()
            except AttributeError:
                self.date = result_date


class Current:
    """Current HIV result/status, but only if POS, returns POS or None"""
    def __init__(self, result=None, evidence=None):
        self.result = None
        if evidence == YES and result == POS:
            self.result = POS


class Recent(Test):
    """HIV result by test at week 32, returns POS, NEG or None.

    within_3m is not inclusive."""
    def __init__(self, reference_datetime=None, evidence=None, **kwargs):
        super(Recent, self).__init__(**kwargs)
        self.within_3m = None
        if evidence == YES and reference_datetime:
            try:
                self.within_3m = self.date > (reference_datetime - relativedelta(months=3)).date()
            except TypeError:
                raise RecentResultError('Invalid dates for within_3m calc.')
            if self.result == NEG and not self.within_3m:
                self.result = None
                self.date = None
                self.within_3m = None
        else:
            self.result = None
            self.date = None


class Rapid(Test):
    """HIV result by rapid test whihc is required if cannot determine POS status by other means."""
    pass
