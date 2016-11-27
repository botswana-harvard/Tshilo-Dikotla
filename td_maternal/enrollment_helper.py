import pytz

from datetime import datetime, time
from dateutil.relativedelta import relativedelta

from django.apps import apps as django_apps
from django.utils import timezone

from edc_constants.constants import NO, YES, POS, NEG

tz = pytz.timezone('UTC')


class EnrollmentError(Exception):
    pass


class EnrollmentHelper(object):

    """Class that determines maternal eligibility based on the protocol specific criteria.

    * Accepts an instance of AntenatalEnrollment or PostnatalEnrollment.
    * is called in the save method of the EnrollmentMixin.
    * makes available the calculated enrollment_hiv_status and date_at_32wks
      which can be saved to the model instance.

    Note: it's assumed the form validates values to avoid raising an EnrollmentError here.
    """

    def __init__(self, obj, exception_cls=None):
        self._date_at_32wks = None
        self._delivery = None
        self._edd = None
        self._enrollment_hiv_status = None
        self._is_eligible = None
        self._ga_lmp_enrollment_wks = None
        self._pending_ultrasound = None
        self._ultrasound = None
        self._unenrolled_reasons = None
        self.exception_cls = exception_cls or EnrollmentError
        self.current_hiv_status = obj.current_hiv_status
        self.evidence_32wk_hiv_status = obj.evidence_32wk_hiv_status
        self.evidence_hiv_status = obj.evidence_hiv_status
        self.is_diabetic = obj.is_diabetic
        self.knows_lmp = obj.knows_lmp
        self.lmp = timezone.make_aware(datetime.combine(obj.last_period_date, time()), timezone=tz)
        self.rapid_test_date = obj.rapid_test_date
        self.rapid_test_done = obj.rapid_test_done
        self.rapid_test_result = obj.rapid_test_result
        self.report_datetime = obj.report_datetime
        self.subject_identifier = obj.subject_identifier
        self.week32_result = obj.week32_result
        self.week32_test = obj.week32_test
        self.week32_test_date = obj.week32_test_date
        self.will_breastfeed = obj.will_breastfeed
        self.will_get_arvs = obj.will_get_arvs
        self.will_remain_onstudy = obj.will_remain_onstudy
        self.is_eligible

    def as_dict(self):
        d = {}
        for attr in dir(self):
            if not attr.startswith('_'):
                d.update({attr: getattr(self, attr)})
        return d

    @property
    def is_eligible(self):
        """Returns True if basic criteria is met for enrollment.

        Potentially required model instances:
            MaternalLabourDel
            MaternalUltraSoundInitial
        """
        if not self._is_eligible:
            self._is_eligible = False
            if self.pending_ultrasound or not self.ultrasound:
                meets_basic_criteria = False
            else:
                meets_basic_criteria = (
                    self.lmp_to_use >= 16 and self.lmp_to_use <= 36 and
                    self.no_chronic_conditions and self.will_breastfeed == YES and
                    self.will_remain_onstudy == YES and self.pass_antenatal_enrollment and
                    self.eligible_after_delivery)
            if meets_basic_criteria and self.enrollment_hiv_status == POS and self.will_get_arvs == YES:
                self._is_eligible = True
            elif meets_basic_criteria and self.enrollment_hiv_status == NEG:
                self._is_eligible = True
            else:
                self._is_eligible = False
        return self._is_eligible

    @property
    def date_at_32wks(self):
        if not self._date_at_32wks:
            try:
                self._date_at_32wks = self.edd - relativedelta(weeks=6)
            except TypeError:
                self._date_at_32wks = None
        return self._date_at_32wks

    @property
    def ga_lmp_enrollment_wks(self):
        if not self._ga_lmp_enrollment_wks:
            try:
                self._ga_lmp_enrollment_wks = int(40 - ((self.edd - self.report_datetime.date()).days / 7))
            except TypeError:
                self._ga_lmp_enrollment_wks = None
        return self._ga_lmp_enrollment_wks

    @property
    def edd(self):
        """Naegele's rule"""
        if not self._edd:
            try:
                self._edd = self.lmp + relativedelta(days=280)
            except TypeError:
                self._edd = None
        return self._edd

    @property
    def test_date_is_on_or_after_32wks(self):
        """Returns True if the test date is on or after 32 weeks gestational age."""
        try:
            if self.week32_test_date > self.rapid_test_date:
                raise self.exception_cls('Rapid test date cannot precede test date on or after 32 weeks')
        except TypeError:
            pass
        try:
            test_date_is_on_or_after_32wks = self.week32_test_date >= self.date_at_32wks
        except TypeError:
            test_date_is_on_or_after_32wks = None
        return test_date_is_on_or_after_32wks

    @property
    def eligible_after_delivery(self):
        eligible_after_delivery = None
        try:
            if self.enrollment_hiv_status == POS and self.delivery.valid_regiment_duration != YES:
                eligible_after_delivery = False
        except AttributeError:
            eligible_after_delivery = None
        return eligible_after_delivery

    @property
    def pass_antenatal_enrollment(self):
        try:
            pass_antenatal_enrollment = self.ultrasound.pass_antenatal_enrollment
        except AttributeError:
            pass_antenatal_enrollment = True
        return pass_antenatal_enrollment

    @property
    def lmp_to_use(self):
        try:
            ga_confirmed = self.ultrasound.ga_confirmed
        except AttributeError:
            ga_confirmed = None
        return self.ga_lmp_enrollment_wks if self.ga_lmp_enrollment_wks else ga_confirmed

    @property
    def enrollment_hiv_status(self):
        """Returns the maternal HIV status at enrollment based on valid combinations
        expected from the form otherwise raises a EnrollmentError. Can only return POS or NEG.

        Note: the EnrollmentError should never be excepted!!"""
        if not self._enrollment_hiv_status:
            pos = self.known_hiv_pos_with_evidence or self.tested_pos_at32wks or self.tested_pos_rapidtest
            neg = (self.tested_neg_at32wks or self.tested_neg_rapidtest or
                   self.tested_neg_previously_result_within_3_months)
            if neg and not pos:
                self._enrollment_hiv_status = NEG
            elif pos and not neg:
                self._enrollment_hiv_status = POS
            else:
                # Case neg and pos OR not neg and not pos
                raise self.exception_cls(
                    'Unable to determine maternal hiv status at enrollment. '
                    'Got current_hiv_status={}, evidence_hiv_status={}, '
                    'rapid_test_done={}, rapid_test_result={}'.format(
                        self.current_hiv_status,
                        self.evidence_hiv_status,
                        self.rapid_test_done,
                        self.rapid_test_result))
        return self._enrollment_hiv_status

    @property
    def known_hiv_pos_with_evidence(self):
        """"""
        if self.current_hiv_status == POS and self.evidence_hiv_status == YES:
            return True
        return False

    @property
    def tested_pos_at32wks(self):
        return self.week32_test == YES and self.week32_result == POS and self.evidence_32wk_hiv_status == YES

    @property
    def tested_pos_rapidtest(self):
        return self.rapid_test_done == YES and self.rapid_test_result == POS

    @property
    def tested_neg_at32wks(self):
        return (self.week32_test == YES and self.test_date_is_on_or_after_32wks and
                self.week32_result == NEG and self.evidence_32wk_hiv_status == YES)

    @property
    def tested_neg_rapidtest(self):
        return self.rapid_test_done == YES and self.rapid_test_result == NEG

    @property
    def tested_neg_previously_result_within_3_months(self):
        """Returns true if the 32 week test date is within 3months else false"""
        return (self.week32_test == YES and self.week32_result == NEG and
                self.week32_test_date > (self.report_datetime.date() - relativedelta(months=3)))

    @property
    def rapid_test_exempt(self):
        """Returns True to indicate that a rapid test is not required, False to indicate a rapid test is required."""
        return self.known_hiv_pos_with_evidence or self.tested_pos_at32wks or self.tested_neg_at32wks

    @property
    def raise_validation_error_for_rapidtest(self):
        if (not self.rapid_test_exempt and self.rapid_test_done != YES and
                self.rapid_test_result not in [POS, NEG] and
                not self.tested_neg_previously_result_within_3_months):
            raise self.exception_cls(
                'A rapid test with a valid result of either POS or NEG is required. Ensure this is the case.')

    @property
    def delivery(self):
        if not self._delivery:
            try:
                MaternalLabourDel = django_apps.get_model('td_maternal', 'MaternalLabourDel')
                self._delivery = MaternalLabourDel.objects.get(
                    registered_subject__subject_identifier=self.subject_identifier)
            except MaternalLabourDel.DoesNotExist:
                pass
        return self._delivery

    @property
    def ultrasound(self):
        """Returns an MaternalUltrasoundInitial instance or None."""
        if not self._ultrasound:
            try:
                MaternalUltrasoundInitial = django_apps.get_model('td_maternal', 'MaternalUltraSoundInitial')
                self._ultrasound = MaternalUltrasoundInitial.objects.get(
                    maternal_visit__appointment__subject_identifier=self.subject_identifier)
            except MaternalUltrasoundInitial.DoesNotExist:
                pass
        return self._ultrasound

    @property
    def pending_ultrasound(self):
        """Return True is subject does not have a ultrasound (instance) and lmp is not known."""
        if not self._pending_ultrasound:
            try:
                self._pending_ultrasound = (not self.ultrasound) and (NO in self.knows_lmp)
            except AttributeError:
                self._pending_ultrasound = None
        return self._pending_ultrasound

    @property
    def no_chronic_conditions(self):
        """Returns True if subject has no chronic conditions."""
        return self.is_diabetic == NO

    @property
    def unenrolled_reasons(self):
        """Returns a tuple (True, None) if mother is eligible."""
        if not self._unenrolled_reasons:
            reasons = []
            if not self.is_eligible:
                reasons = ['Diabetic'] if self.is_diabetic == YES else []
                if self.will_breastfeed == NO:
                    reasons.append('will not breastfeed')
                if self.will_remain_onstudy == NO:
                    reasons.append('won\'t remain in study')
                if self.will_get_arvs == NO:
                    reasons.append('Will not get ARVs on this pregnancy.')
                if self.rapid_test_done == NO:
                    reasons.append('rapid test not done')
                if self.ga_lmp_enrollment_wks and (self.ga_lmp_enrollment_wks < 16 or self.ga_lmp_enrollment_wks > 36):
                    reasons.append('gestation not 16 to 36wks')
                if self.delivery and not self.eligible_after_delivery:
                    reasons.append('Hiv+ and not on ART for atleast 4 weeks.')
                if self.ultrasound and not self.pass_antenatal_enrollment:
                    reasons.append('Pregnancy is not a singleton.')
            self._unenrolled_reasons = reasons
        return self._unenrolled_reasons
