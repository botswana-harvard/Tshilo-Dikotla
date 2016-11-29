import pytz

from datetime import time, datetime
from dateutil.relativedelta import relativedelta

from django.apps import apps as django_apps

from edc_constants.constants import NO, YES, POS, NEG, NOT_APPLICABLE
from edc_pregnancy_utils import Edd, Ga, Lmp, Ultrasound

from td.hiv_status import EnrollmentStatus


class EnrollmentError(Exception):
    pass


class NotEligibleError(Exception):
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
        self.messages = {}
        self._date_at_32wks = None
        self._pending_ultrasound = None
        self._unenrolled_reasons = None
        self.exception_cls = exception_cls or EnrollmentError
        self.current_hiv_status = obj.current_hiv_status
        self.evidence_hiv_status = obj.evidence_hiv_status
        self.knows_lmp = obj.knows_lmp
        self.will_breastfeed = obj.will_breastfeed
        self.will_remain_onstudy = obj.will_remain_onstudy
        self.is_diabetic = obj.is_diabetic
        self.will_get_arvs = obj.will_get_arvs
        self.report_datetime = obj.report_datetime
        self.subject_identifier = obj.subject_identifier
        self.last_period_date = obj.last_period_date
        MaternalLabourDel = django_apps.get_model('td_maternal', 'MaternalLabourDel')
        MaternalUltraSoundInitial = django_apps.get_model('td_maternal', 'MaternalUltraSoundInitial')

        # hiv status
        self.enrollment_status = EnrollmentStatus(obj)
        self.enrollment_hiv_status = self.enrollment_status.result
        if self.enrollment_status.result not in [POS, NEG]:
            self.messages.update(lmp='Unable to determine HIV status')
            if not self.enrollment_status.rapid.result:
                self.messages.update(lmp='Rapid test not done')

        # check if values are paired correctly. (these problems should be captured on the modelform)
        if self.enrollment_status.result == POS and self.will_get_arvs in [NOT_APPLICABLE, NO]:
            self.messages.update(
                will_get_arvs='will_get_arvs must be YES for HIV status = POS. Got {}'.format(self.will_get_arvs))
        if self.enrollment_status.result == NEG and self.will_get_arvs != NOT_APPLICABLE:
            self.messages.update(
                will_get_arvs='will_get_arvs must be N/A for HIV status = NEG. Got {}'.format(self.will_get_arvs))
        if self.knows_lmp and not self.last_period_date:
            self.messages.update(
                last_period_date='last_period_date may not be None if knows_lmp == YES')

        # check if delivered, and if so, was mother on art for 4 weeks during pregnancy
        try:
            obj = MaternalLabourDel.objects.get(
                registered_subject__subject_identifier=self.subject_identifier)
            self.on_art_4wks_in_pregnancy = obj.valid_regiment_duration
            if self.on_art_4wks_in_pregnancy == NO:
                self.messages.update(
                    on_art_4wks_in_pregnancy='Mother was not on ART for at least 4 weeks during pregnancy')
        except MaternalLabourDel.DoesNotExist:
            self.on_art_4wks_in_pregnancy = None

        # ultrasound
        try:
            obj = MaternalUltraSoundInitial.objects.get(
                maternal_visit__appointment__subject_identifier=self.subject_identifier)
            self.ultrasound = Ultrasound(
                ultrasound_date=obj.report_datetime,
                ga_weeks=obj.ga_by_ultrasound_wks,
                ga_days=obj.ga_by_ultrasound_days)
            self.ultrasound.gestations = int(obj.number_of_gestations)
            if self.ultrasound.gestations != 1:
                self.messages.update(will_get_arvs='Pregnancy is not a singleton.')
        except MaternalUltraSoundInitial.DoesNotExist:
            self.ultrasound = Ultrasound()

        # lmp, ga and edd. Only ga for eligibility
        if obj.last_period_date:
            self.lmp = Lmp(
                lmp=pytz.utc.localize(datetime.combine(obj.last_period_date, time())),
                reference_date=self.ultrasound.date)
        else:
            self.lmp = Lmp()
        self.ga = Ga(lmp=self.lmp, ultrasound=self.ultrasound)
        self.edd = Edd(lmp=self.lmp, ultrasound=self.ultrasound)
        self.edd_confirmation_method = self.edd.edd_confirmation_method
        try:
            if not 16 < self.lmp.ga <= 36:
                self.messages.update(lmp='gestation not 16 to 36wks')
        except TypeError:
            self.messages.update(lmp='Unable to determine GA')

        # how does this work into eligibility?
        try:
            self.test_date_on_or_after_32wks = self.enrollment_status.week32.date >= self.date_at_32wks
        except TypeError:
            self.test_date_on_or_after_32wks = None

        # what is a pending ultrasound and how does the affect eligibility?

        # where does date_at_32wks work in?

        # simple criteria that makes ineligible regardless of other values
        if self.will_get_arvs == NO:
            self.messages.update(will_get_arvs='Will not get ARVs on this pregnancy.')
        if self.will_breastfeed == NO:
            self.messages.update(will_breastfeed='Will not breastfeed')
        if self.will_remain_onstudy == NO:
            self.messages.update(will_remain_onstudy='Will not remain on-study')
        if self.is_diabetic == YES:
            self.messages.update(is_diabetic='Is diabetic')

        # that's it
        self.is_eligible = True if self.messages else False

    def as_dict(self):
        d = {}
        for attr in dir(self):
            if not attr.startswith('_'):
                d.update({attr: getattr(self, attr)})
        return d

    @property
    def date_at_32wks(self):
        """???????"""
        if not self._date_at_32wks:
            try:
                self._date_at_32wks = self.edd - relativedelta(weeks=6)
            except TypeError:
                self._date_at_32wks = None
        return self._date_at_32wks

    @property
    def pending_ultrasound(self):
        """???????"""
        """Return True is subject does not have a ultrasound (instance) and lmp is not known."""
        if not self._pending_ultrasound:
            try:
                self._pending_ultrasound = (not self.ultrasound) and (self.knows_lmp == NO)
            except AttributeError:
                self._pending_ultrasound = None
        return self._pending_ultrasound
