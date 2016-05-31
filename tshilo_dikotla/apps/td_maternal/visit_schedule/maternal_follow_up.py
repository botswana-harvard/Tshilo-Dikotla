from collections import OrderedDict

from edc_visit_schedule.classes import (
    VisitScheduleConfiguration, site_visit_schedules, MembershipFormTuple, ScheduleTuple)

from ..models import MaternalLabourDel, MaternalVisit

from .entries import maternal_antenatal1_entries, maternal_requisition_entries


class MaternalFollowUpSchedule(VisitScheduleConfiguration):

    name = 'Follow up visit schedule'
    app_label = 'td_maternal'

    membership_forms = OrderedDict({'follow_up': MembershipFormTuple(
        'follow_up', MaternalLabourDel, True), })

    schedules = OrderedDict({
        'Follow Up Visit': ScheduleTuple('Follow Up Visit', 'follow_up', None, None), })

    visit_definitions = OrderedDict()

    visit_definitions['1100M'] = {
        'title': '1 Month Visit',
        'time_point': 30,
        'base_interval': 10,
        'base_interval_unit': 'D',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': (),
        'entries': maternal_antenatal1_entries}

    visit_definitions['1200M'] = {
        'title': '2 Months Visit',
        'time_point': 50,
        'base_interval': 12,
        'base_interval_unit': 'D',
        'window_lower_bound': 15,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 60,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': (),
        'entries': maternal_antenatal1_entries}

    visit_definitions['1600M'] = {
        'title': '6 Months Visit',
        'time_point': 110,
        'base_interval': 16,
        'base_interval_unit': 'D',
        'window_lower_bound': 29,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 45,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': (),
        'entries': maternal_antenatal1_entries}

    visit_definitions['2200M'] = {
        'title': '12 Months Visit',
        'time_point': 170,
        'base_interval': 22,
        'base_interval_unit': 'D',
        'window_lower_bound': 44,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 45,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': (),
        'entries': maternal_antenatal1_entries}

    visit_definitions['2800M'] = {
        'title': '18 Months Visit',
        'time_point': 230,
        'base_interval': 28,
        'base_interval_unit': 'D',
        'window_lower_bound': 44,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 45,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': (),
        'entries': maternal_antenatal1_entries}

    visit_definitions['2400M'] = {
        'title': '24 Months Visit',
        'time_point': 290,
        'base_interval': 34,
        'base_interval_unit': 'D',
        'window_lower_bound': 44,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 45,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': (),
        'entries': maternal_antenatal1_entries}

    visit_definitions['3000M'] = {
        'title': '30 Months Visit',
        'time_point': 350,
        'base_interval': 40,
        'base_interval_unit': 'D',
        'window_lower_bound': 44,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 45,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': (),
        'entries': maternal_antenatal1_entries}

    visit_definitions['3600M'] = {
        'title': '36 Months Visit',
        'time_point': 410,
        'base_interval': 46,
        'base_interval_unit': 'D',
        'window_lower_bound': 44,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 45,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': (),
        'entries': maternal_antenatal1_entries}

site_visit_schedules.register(MaternalFollowUpSchedule)
