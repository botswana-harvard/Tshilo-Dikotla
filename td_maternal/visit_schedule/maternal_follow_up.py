from collections import OrderedDict

from edc_visit_schedule.classes import (
    VisitScheduleConfiguration, site_visit_schedules, MembershipFormTuple, ScheduleTuple)

from ..models import MaternalLabourDel, MaternalVisit

from .entries import (maternal_birth_entries, maternal_followup1_entries, maternal_followup2_entries,
                      maternal_followup3_entries, maternal_requisition_followup)


class MaternalFollowUpSchedule(VisitScheduleConfiguration):

    name = 'Follow up visit schedule'
    app_label = 'td_maternal'

    membership_forms = OrderedDict({'follow_up': MembershipFormTuple(
        'follow_up', MaternalLabourDel, True), })

    schedules = OrderedDict({
        'Follow Up Visit': ScheduleTuple('Follow Up Visit', 'follow_up', None, None), })

    visit_definitions = OrderedDict()

    visit_definitions['2000M'] = {
        'title': 'Delivery Visit',
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
        'requisitions': maternal_requisition_followup,
        'entries': maternal_birth_entries}

    visit_definitions['2010M'] = {
        'title': '1 Months Visit',
        'time_point': 50,
        'base_interval': 1,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': maternal_requisition_followup,
        'entries': maternal_followup1_entries}

    visit_definitions['2020M'] = {
        'title': '2 Months Visit',
        'time_point': 110,
        'base_interval': 2,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': maternal_requisition_followup,
        'entries': maternal_followup1_entries}

    visit_definitions['2060M'] = {
        'title': '6 Months Visit',
        'time_point': 170,
        'base_interval': 6,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': maternal_requisition_followup,
        'entries': maternal_followup1_entries}

    visit_definitions['2120M'] = {
        'title': '12 Months Visit',
        'time_point': 230,
        'base_interval': 12,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': maternal_requisition_followup,
        'entries': maternal_followup2_entries}

    visit_definitions['2180M'] = {
        'title': '18 Months Visit',
        'time_point': 290,
        'base_interval': 18,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': maternal_requisition_followup,
        'entries': maternal_followup3_entries}

    visit_definitions['2240M'] = {
        'title': '24 Months Visit',
        'time_point': 350,
        'base_interval': 24,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': maternal_requisition_followup,
        'entries': maternal_followup3_entries}

    visit_definitions['2300M'] = {
        'title': '30 Months Visit',
        'time_point': 410,
        'base_interval': 30,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': maternal_requisition_followup,
        'entries': maternal_followup3_entries}

    visit_definitions['2360M'] = {
        'title': '36 Months Visit',
        'time_point': 410,
        'base_interval': 36,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Follow Up Visit',
        'instructions': '',
        'requisitions': maternal_requisition_followup,
        'entries': maternal_followup3_entries}

site_visit_schedules.register(MaternalFollowUpSchedule)
