import pytz

from collections import OrderedDict
from datetime import time, datetime

from django.apps import apps as django_apps

from edc_constants.constants import NO, YES, NEG, POS, NOT_APPLICABLE
from edc_pregnancy_utils import Edd, Ga, Lmp, Ultrasound

from td.hiv_result import (
    Enrollment as EnrollmentResult, Recent, Rapid, Current, EnrollmentNoResultError,
    EnrollmentRapidTestRequiredError)


class EnrollmentError(Exception):
    pass


class Messages(OrderedDict):

    def as_string(self):
        return ', '.join(self.values())


class EnrollmentHelper(object):

    """Class that determines maternal eligibility."""

    def __init__(self, obj, exception_cls=None):
        self._delivery = None
        self._ultrasound = None
        self.edd = None
        self.enrollment_result = None
        self.exception_cls = exception_cls or EnrollmentError
        self.ga = None
        self.ga_pending = False
        self.is_eligible = None
        self.lmp = None
        self.messages = Messages()
        self.on_art_4wks_in_pregnancy = None
        self.subject_identifier = obj.subject_identifier

        # enrollment HIV result
        try:
            self.enrollment_result = self.get_enrollment_result(obj)
        except EnrollmentNoResultError as e:
            self.messages.update(enrollment_result=str(e))
        except EnrollmentRapidTestRequiredError as e:
            self.messages.update(enrollment_result=str(e))

        # check if delivered, and if so, was mother on art for 4 weeks during pregnancy
        try:
            self.on_art_4wks_in_pregnancy = self.delivery.valid_regiment_duration
            if self.on_art_4wks_in_pregnancy == NO:
                self.messages.update(
                    on_art_4wks_in_pregnancy='Mother was not on ART for at least 4 weeks during pregnancy')
        except AttributeError:
            self.on_art_4wks_in_pregnancy = None

        # lmp, ga and edd. Only ga for eligibility
        if obj.last_period_date:
            self.lmp = Lmp(
                lmp=pytz.utc.localize(datetime.combine(obj.last_period_date, time())),
                reference_date=self.ultrasound.report_date or obj.report_datetime)
        else:
            self.lmp = Lmp()
        self.ga = Ga(lmp=self.lmp, ultrasound=self.ultrasound)
        self.edd = Edd(lmp=self.lmp, ultrasound=self.ultrasound)
        try:
            if not 16 < self.ga.weeks <= 36:
                self.messages.update(ga='gestation not 16 to 36wks')
        except TypeError as e:
            # if GA not known or invalid, allow enrollment to continue, but set this flag for future reference.
            self.ga_pending = True

        # simple criteria that makes ineligible regardless of other values
        if obj.will_get_arvs == NO:
            self.messages.update(will_get_arvs='Will not get ARVs on this pregnancy.')
        if obj.will_breastfeed == NO:
            self.messages.update(will_breastfeed='Will not breastfeed')
        if obj.will_remain_onstudy == NO:
            self.messages.update(will_remain_onstudy='Will not remain on-study')
        if obj.is_diabetic == YES:
            self.messages.update(is_diabetic='Is diabetic')

        # check if values are paired correctly. (these problems should be captured on the modelform)
        # and maybe dont belong here
        if self.enrollment_result.result == POS and obj.will_get_arvs in [NOT_APPLICABLE, NO]:
            self.messages.update(
                will_get_arvs='will_get_arvs must be YES for HIV status = POS. Got {}'.format(obj.will_get_arvs))
        if self.enrollment_result.result == NEG and obj.will_get_arvs != NOT_APPLICABLE:
            self.messages.update(
                will_get_arvs='will_get_arvs must be N/A for HIV status = NEG. Got {}'.format(obj.will_get_arvs))
        if obj.knows_lmp and not obj.last_period_date:
            self.messages.update(
                last_period_date='last_period_date may not be None if knows_lmp == YES')

        # that's it
        self.is_eligible = False if self.messages else True

    def as_dict(self):
        d = {}
        for attr in dir(self):
            if not attr.startswith('_'):
                d.update({attr: getattr(self, attr)})
        return d

    def get_enrollment_result(self, obj):
        """Returns a populated EnrollmentResult instance where enrollment_result.result
        is the final result."""
        current = Current(
            result=obj.current_hiv_status,
            evidence=obj.evidence_hiv_status)
        recent = Recent(
            reference_datetime=obj.report_datetime,
            evidence=obj.evidence_32wk_hiv_status,
            tested=obj.week32_test,
            result=obj.week32_result,
            result_date=obj.week32_test_date)
        rapid = Rapid(
            tested=obj.rapid_test_done,
            result=obj.rapid_test_result,
            result_date=obj.rapid_test_result)
        return EnrollmentResult(current=current, recent=recent, rapid=rapid)

    @property
    def ultrasound(self):
        """Returns an Ultrasound instance."""
        if not self._ultrasound:
            MaternalUltraSoundInitial = django_apps.get_model('td_maternal', 'MaternalUltraSoundInitial')
            try:
                obj = MaternalUltraSoundInitial.objects.get(
                    maternal_visit__appointment__subject_identifier=self.subject_identifier)
                self._ultrasound = Ultrasound(
                    ultrasound_date=obj.report_datetime,
                    ga_weeks=obj.ga_by_ultrasound_wks,
                    ga_days=obj.ga_by_ultrasound_days)
                self._ultrasound.gestations = int(obj.number_of_gestations)
                if self._ultrasound.gestations != 1:
                    self.messages.update(will_get_arvs='Pregnancy is not a singleton.')
            except MaternalUltraSoundInitial.DoesNotExist:
                self._ultrasound = Ultrasound()
        return self._ultrasound

    @property
    def delivery(self):
        """Returns a MaternalLabourDel instance or None."""
        if not self._delivery:
            MaternalLabourDel = django_apps.get_model('td_maternal', 'MaternalLabourDel')
            try:
                self.delivery = MaternalLabourDel.objects.get(
                    subject_identifier=self.subject_identifier)
            except MaternalLabourDel.DoesNotExist:
                self._delivery = None
        return self._delivery
