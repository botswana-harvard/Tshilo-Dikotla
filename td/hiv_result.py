from dateutil.relativedelta import relativedelta

from edc_constants.constants import YES, POS, NEG, IND


class EnrollmentResultError(Exception):
    pass


class PostEnrollmentResultError(Exception):
    pass


class ElisaRequiredError(Exception):
    pass


class EnrollmentNoResultError(Exception):
    pass


class RapidTestRequiredError(Exception):
    pass


class RecentResultError(Exception):
    pass


class EnrollmentResult:
    """Determines hiv status for enrollment, returns POS, NEG.

    A final result of None raises an error.

    Raises an exception if a rapid test or ELISA is required."""
    def __init__(self, reference_datetime=None, current=None, recent=None, rapid=None, exception_cls=None):
        self.result = None
        self.result_date = None
        self.exception_cls = exception_cls or EnrollmentResultError
        try:
            self.current = Current(
                reference_datetime=reference_datetime,
                result=current.result,
                result_date=current.result_date,
                evidence=current.tested)
        except AttributeError:
            self.current = Current()
        try:
            self.recent = Recent(
                reference_datetime=reference_datetime,
                result=recent.result,
                result_date=recent.result_date,
                evidence=recent.tested)
        except AttributeError:
            self.recent = Recent()
        try:
            self.rapid = Rapid(
                reference_datetime=reference_datetime,
                result=rapid.result,
                result_date=rapid.result_date)
        except AttributeError:
            self.rapid = Rapid()
        if not self.current.result and not self.recent.result and not self.rapid.result:
            raise RapidTestRequiredError(
                'Rapid test is required if result is not known or no longer valid.')
        else:
            try:
                if self.recent.result_date > self.rapid.result_date:
                    raise self.exception_cls(
                        'Rapid test result_date cannot precede test result_date on or after 32 weeks')
            except TypeError:
                pass
            if self.current.result == POS or self.recent.result == POS or self.rapid.result == POS:
                self.result = POS
                results = [obj for obj in [self.current, self.recent, self.rapid] if obj.result == POS]
                results.sort(key=lambda test: test.result_date)
                self.result_date = results[0].result_date
            elif self.rapid.result == NEG or self.recent.result == NEG:
                self.result = NEG
                results = [obj for obj in [self.current, self.recent, self.rapid] if obj.result == NEG]
                results.sort(key=lambda test: test.result_date)
                self.result_date = results[-1:][0].result_date
            if self.current.result != POS and self.recent.result != POS:
                if not self.rapid.result:
                    raise self.exception_cls(
                        'A rapid test result is required. Got current.result == {}, recent.result == {}'.format(
                            self.current.result, self.recent.result))
            if not self.result:
                raise RapidTestRequiredError(
                    'Rapid test is required if result is not known or no longer valid.')
            elif self.result == IND:
                raise ElisaRequiredError('ELISA is required to resolve indeterminate HIV result.')
            elif self.result not in [POS, NEG]:
                if self.rapid.result:
                    raise EnrollmentNoResultError(
                        'Unable to determine a POS or NEG result. Got {}.'.format(self.result))
                else:
                    raise RapidTestRequiredError('Rapid test is required if result is not known or no longer valid.')


class Test:
    """Basic Test Result"""
    def __init__(self, tested=None, result=None, result_date=None):
        self.result_date = None
        self.result = None
        self.tested = None
        if tested == YES and result_date and result:
            self.result = result
            self.tested = YES
            try:
                self.result_date = result_date.date()
            except AttributeError:
                self.result_date = result_date


class Recent(Test):
    """HIV result within 3m returns POS, NEG or None.

    within_3m is not inclusive."""
    def __init__(self, reference_datetime=None, evidence=None, **kwargs):
        kwargs.update(tested=evidence)
        super(Recent, self).__init__(**kwargs)
        self.within_3m = None
        if self.result_date and evidence == YES and reference_datetime:
            try:
                self.within_3m = self.result_date > (reference_datetime - relativedelta(months=3)).date()
            except TypeError:
                raise RecentResultError(
                    'Invalid dates for within_3m calc. Got reference_datetime={} and result_date={}'.format(
                        reference_datetime, self.result_date))
            if self.result in [NEG, IND] and not self.within_3m:
                self.result = None
                self.result_date = None
                self.tested = None
                self.within_3m = None
        else:
            self.result = None
            self.result_date = None
            self.tested = None
            self.within_3m = None


class Current(Recent):
    """Current HIV result/status, but only if POS, returns POS or None."""
    def __init__(self, reference_datetime=None, result=None, result_date=None, evidence=None):
        super(Current, self).__init__(
            reference_datetime=reference_datetime,
            evidence=evidence,
            result=result,
            result_date=result_date)
        if self.result != POS:
            self.result = None
            self.result_date = None
            self.tested = None
            self.within_3m = None


class Rapid(Recent):
    """HIV result by rapid test whihc is required if cannot determine POS status by other means."""
    def __init__(self, reference_datetime=None, result=None, result_date=None):
        super(Rapid, self).__init__(
            reference_datetime=reference_datetime,
            evidence=YES,
            result=result,
            result_date=result_date)


class PostEnrollmentResult:
    """Determines hiv status anytime post-enrollment, returns POS, NEG or None."""
    def __init__(self, reference_datetime=None, enrollment_result=None, rapid_results=None, exception_cls=None):
        rapid_results = [] if not rapid_results else list(rapid_results)
        self.result = None
        self.result_date = None
        self.reference_datetime = reference_datetime
        self.enrollment_result = enrollment_result or Recent()
        self.enrollment_result = Recent(
            reference_datetime=reference_datetime,
            result=self.enrollment_result.result,
            result_date=self.enrollment_result.result_date,
            tested=YES, evidence=YES)
        self.exception_cls = exception_cls or PostEnrollmentResultError
        if self.enrollment_result.result == POS:
            # POS at enrollment ... we're done.
            self.result = self.enrollment_result.result
            self.result_date = self.enrollment_result.result_date
        else:
            # filter for POS results
            try:
                pos_rapid_results = [test for test in rapid_results if test.result == POS]
            except TypeError:
                pos_rapid_results = []
            # order POS results to select first
            pos_rapid_results.sort(key=lambda test: test.result_date)
            if pos_rapid_results:
                # select first POS
                self.result = pos_rapid_results[0].result
                self.result_date = pos_rapid_results[0].result_date
            else:
                # not POS so ...
                # select tests within last three months
                recent_results = []
                if self.enrollment_result.result == NEG:
                    recent = Recent(
                        reference_datetime=reference_datetime,
                        result=enrollment_result.result,
                        result_date=enrollment_result.result_date,
                        tested=YES, evidence=YES)
                    if recent.result in [NEG, IND]:
                        recent_results.append(recent)
                for test in rapid_results:
                    recent = Recent(
                        reference_datetime=reference_datetime,
                        result=test.result,
                        result_date=test.result_date,
                        tested=YES, evidence=YES)
                    if recent.result in [NEG, IND]:
                        recent_results.append(recent)
                # sort NEG/IND results reversed by date
                recent_results.sort(key=lambda test: test.result_date, reverse=True)
                if recent_results:
                    # select most recent result (not POS)
                    self.result = recent_results[0].result
                    self.result_date = None if not self.result else recent_results[0].result_date
                    if self.result == IND:
                        raise ElisaRequiredError('Elisa test is required for indeterminate result.')
