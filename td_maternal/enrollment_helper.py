from datetime import datetime, time
from dateutil.relativedelta import relativedelta

from django.apps import apps as django_apps
from django.utils import timezone

from edc_constants.constants import NO, YES, POS, NEG, NOT_APPLICABLE
from edc_pregnancy_utils import Edd, Ga, Lmp

from td.hiv_status import EnrollmentStatus


class EnrollmentError(Exception):
    pass


class EnrollmentHelper(object):

    """Class that determines maternal eligibility based on the protocol specific criteria.

    * Accepts an instance of AntenatalEnrollment or PostnatalEnrollment.
    * is called in the save method of the EnrollmentMixin.
    * makes available the calculated enrollment_hiv_status and date_at_32wks
      which can be saved to the model instance.

    Note: it's assumed the form validates values to avoid raising an EnrollmentError here.

    subject_identifier
    report_datetime

    last_period_date (if know, 16-36 weeks)

    current_hiv_status
    evidence_hiv_status

    evidence_32wk_hiv_status
    week32_result
    week32_test
    week32_test_date

    # required if current_hiv_status == NEG
    rapid_test_date
    rapid_test_done
    rapid_test_result

    knows_lmp

    will_get_arvs (if NO, not eligible, if POS->YES, if NEG->N/A)
    is_diabetic (if NO, not eligible)
    will_breastfeed  (if NO, not eligible)
    will_remain_onstudy  (if NO, not eligible)
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
        self.evidence_hiv_status = obj.evidence_hiv_status
        self.knows_lmp = obj.knows_lmp
        if obj.last_period_date:
            self.lmp = Lmp(timezone.make_aware(datetime.combine(obj.last_period_date, time())))
        else:
            self.lmp = None

        self.report_datetime = obj.report_datetime
        self.subject_identifier = obj.subject_identifier

        # hiv status
        enrollment_status = EnrollmentStatus(obj)
        self.enrollment_hiv_status = enrollment_status.result
        # what was this for?
        try:
            self.test_date_on_or_after_32wks = enrollment_status.week32.date >= self.date_at_32wks
        except TypeError:
            self.test_date_on_or_after_32wks = None

        # simple criteria that makes ineligible regardless of other values
        self.will_breastfeed = obj.will_breastfeed
        self.will_remain_onstudy = obj.will_remain_onstudy
        self.is_diabetic = obj.is_diabetic
        self.will_get_arvs = obj.will_get_arvs
        if self.will_get_arvs == NO:
            self._is_eligible = False
        if self.will_breastfeed == NO:
            self._is_eligible = False
        if self.will_remain_onstudy == NO:
            self._is_eligible = False
        if self.is_diabetic == NO:
            self._is_eligible = False

        # expected paired values
        if self.enrollment_hiv_status == POS and self.will_get_arvs != YES:
            raise EnrollmentError('will_get_arvs must be YES for HIV status = POS')
        if self.enrollment_hiv_status == NEG and self.will_get_arvs != NOT_APPLICABLE:
            raise EnrollmentError('will_get_arvs must be N/A for HIV status = NEG')

        # run
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
        if self._is_eligible is None:
            self._is_eligible = False
            if self.pending_ultrasound or not self.ultrasound:
                meets_basic_criteria = False
            else:
                meets_basic_criteria = (
                    self.lmp_to_use >= 16 and self.lmp_to_use <= 36 and
                    self.pass_antenatal_enrollment and
                    self.eligible_after_delivery)
            if meets_basic_criteria and self.enrollment_hiv_status == POS:
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
                self._pending_ultrasound = (not self.ultrasound) and (self.knows_lmp == NO)
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
