from collections import OrderedDict

from edc_visit_schedule.classes import (
    VisitScheduleConfiguration, site_visit_schedules, MembershipFormTuple, ScheduleTuple)

from ..models import AntenatalVisitMembership, MaternalVisit

from .entries import maternal_antenatal_entries, maternal_requisition_entries


class AntenatalVisitSchedule(VisitScheduleConfiguration):

    name = 'Antenatal visit schedule'
    app_label = 'td_maternal'

    membership_forms = OrderedDict({'antenatal': MembershipFormTuple(
        'antenatal', AntenatalVisitMembership, True), })

    schedules = OrderedDict({
        'Antenatal Visit': ScheduleTuple('Antenatal Visit', 'antenatal', None, None), })

    visit_definitions = OrderedDict()

    visit_definitions['1100M'] = {
        'title': 'Antenatal Visit 1',
        'time_point': 0,
        'base_interval': 1,
        'base_interval_unit': 'D',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Antenatal Visit',
        'instructions': '',
        'requisitions': maternal_requisition_entries,
        'entries': maternal_antenatal_entries}

    visit_definitions['1200M'] = {
        'title': 'Antenatal Visit 2',
        'time_point': 10,
        'base_interval': 3,
        'base_interval_unit': 'D',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Antenatal Visit',
        'instructions': '',
        'requisitions': (),
        'entries': maternal_antenatal_entries}

site_visit_schedules.register(AntenatalVisitSchedule)
