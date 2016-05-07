from collections import OrderedDict

from edc_visit_schedule.classes import (
    VisitScheduleConfiguration, site_visit_schedules, MembershipFormTuple, ScheduleTuple)

from ..models import AntenatalEnrollment, MaternalVisit

from .entries import maternal_history_entries, maternal_requisition_entries


class AntenatalEnrollmentVisitSchedule(VisitScheduleConfiguration):

    name = 'antenatal visit schedule'
    app_label = 'mb_maternal'

    membership_forms = OrderedDict({'antenatal': MembershipFormTuple(
        'antenatal', AntenatalEnrollment, True), })

    schedules = OrderedDict({
        'Antenatal Enrollment': ScheduleTuple('Antenatal Enrollment',
                                              'antenatal', None, None), })

    visit_definitions = OrderedDict()

#     visit_definitions['1000M'] = {
#         'title': 'Maternal Patient History',
#         'time_point': 0,
#         'base_interval': 0,
#         'base_interval_unit': 'D',
#         'window_lower_bound': 0,
#         'window_lower_bound_unit': 'D',
#         'window_upper_bound': 0,
#         'window_upper_bound_unit': 'D',
#         'grouping': 'maternal',
#         'visit_tracking_model': MaternalVisit,
#         'schedule': 'Antenatal Enrollment',
#         'instructions': '',
#         'requisitions': maternal_requisition_entries,
#         'entries': maternal_history_entries}

site_visit_schedules.register(AntenatalEnrollmentVisitSchedule)
