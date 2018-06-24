from collections import OrderedDict

from edc_visit_schedule.classes import (
    VisitScheduleConfiguration, site_visit_schedules, MembershipFormTuple, ScheduleTuple)

from ..models import AntenatalVisitMembership, MaternalVisit

from .entries import (maternal_antenatal1_entries,
                      maternal_antenatal2_entries, maternal_requisition_antenatal1,
                      maternal_requisition_antenatal2)


class AntenatalVisitScheduleV3(VisitScheduleConfiguration):

    name = 'Antenatal visit schedule v3'
    app_label = 'td_maternal'

    membership_forms = OrderedDict({'antenatalv3': MembershipFormTuple(
        'antenatalv3', AntenatalVisitMembership, True), })

    schedules = OrderedDict({
        'Antenatal Visit v3': ScheduleTuple('Antenatal Visit v3', 'antenatalv3', None, None), })

    visit_definitions = OrderedDict()

    visit_definitions['1010M'] = {
        'title': 'Antenatal Visit 1 v3',
        'time_point': 5,
        'base_interval': 1,
        'base_interval_unit': 'D',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule': 'Antenatal Visit',
        'instructions': 'V3',
        'requisitions': maternal_requisition_antenatal1,
        'entries': maternal_antenatal1_entries}

    visit_definitions['1020M'] = {
        'title': 'Antenatal Visit 2 v3',
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
        'instructions': 'V3',
        'requisitions': maternal_requisition_antenatal2,
        'entries': maternal_antenatal2_entries}

site_visit_schedules.register(AntenatalVisitScheduleV3)
