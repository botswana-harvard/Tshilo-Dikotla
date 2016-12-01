from dateutil.relativedelta import relativedelta

from edc_constants.constants import YES, POS, NEG


class EnrollmentResultError(Exception):
    pass


class PostEnrollmentResultError(Exception):
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
            if self.recent.result_date > self.rapid.result_date:
                raise self.exception_cls('Rapid test result_date cannot precede test result_date on or after 32 weeks')
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
    """Basic Test Result"""
    def __init__(self, tested=None, result=None, result_date=None):
        self.result_date = None
        self.result = None
        if tested == YES and result_date and result:
            self.result = result
            try:
                self.result_date = result_date.date()
            except AttributeError:
                self.result_date = result_date


class Current:
    """Current HIV result/status, but only if POS, returns POS or None"""
    def __init__(self, result=None, evidence=None):
        self.result = None
        if evidence == YES and result == POS:
            self.result = POS


class Recent(Test):
    """HIV result within 3m returns POS, NEG or None.

    within_3m is not inclusive."""
    def __init__(self, reference_datetime=None, evidence=None, **kwargs):
        super(Recent, self).__init__(**kwargs)
        self.within_3m = None
        if evidence == YES and reference_datetime:
            try:
                self.within_3m = self.result_date > (reference_datetime - relativedelta(months=3)).date()
            except TypeError:
                raise RecentResultError('Invalid dates for within_3m calc.')
            if self.result == NEG and not self.within_3m:
                self.result = None
                self.result_date = None
                self.within_3m = None
        else:
            self.result = None
            self.result_date = None


class Rapid(Test):
    """HIV result by rapid test whihc is required if cannot determine POS status by other means."""
    pass


class PostEnrollment:
    """Determines hiv status anytime post-enrollment, returns POS, NEG or None."""
    def __init__(self, reference_datetime, enrollment_result, rapid_results, exception_cls=None):
        self.result = None
        self.result_date = None
        self.reference_datetime = reference_datetime
        self.enrollment_result = enrollment_result
        self.exception_cls = exception_cls or PostEnrollmentResultError
        if self.enrollment_result == POS:
            # POS at enrollment ... we're done.
            self.result = self.enrollment_result
            self.result_date = None
        else:
            # filter for POS results
            pos_rapid_results = [test for test in rapid_results if test.result == POS]
            # order POS results to select first
            pos_rapid_results.sort(key=lambda test: test.result_date)
            if pos_rapid_results:
                # select first POS
                self.result, self.result_date = pos_rapid_results[0].result, pos_rapid_results[0].result_date
            else:
                # select tests within last three months
                opts = dict(tested=YES, evidence=YES)
                recent_results = []
                for test in rapid_results:
                    recent = Recent(
                        reference_datetime=reference_datetime,
                        result=test.result,
                        result_date=test.result_date, **opts)
                    if recent.result:
                        recent_results.append(recent)
                # sort reversed by date
                recent_results.sort(key=lambda test: test.result_date, reverse=True)
                if recent_results:
                    # select most recent result (not POS)
                    self.result, self.result_date = recent_results[0].result, recent_results[0].result_date
