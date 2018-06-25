from collections import OrderedDict

from edc_visit_schedule.classes import (
    VisitScheduleConfiguration, site_visit_schedules, MembershipFormTuple, ScheduleTuple)

from ..models import AntenatalEnrollment, MaternalVisit

from .entries import maternal_enrollment_entries


class AntenatalEnrollmentVisitScheduleV3(VisitScheduleConfiguration):

    name = 'enrollment visit schedule v3'
    app_label = 'td_maternal'

    membership_forms = OrderedDict({'enrollmentv3': MembershipFormTuple(
        'enrollmentv3', AntenatalEnrollment, True), })

    schedules = OrderedDict({
        'Antenatal Enrollment v3': ScheduleTuple('Antenatal Enrollment v3',
                                              'enrollmentv3', None, None), })

    visit_definitions = OrderedDict()

    visit_definitions['1000M'] = {
        'title': 'Maternal Enrollment Visit v3',
        'time_point': 0,
        'base_interval': 0,
        'base_interval_unit': 'D',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Antenatal Enrollment',
        'instructions': 'V3',
        'requisitions': (),
        'entries': maternal_enrollment_entries}

site_visit_schedules.register(AntenatalEnrollmentVisitScheduleV3)
