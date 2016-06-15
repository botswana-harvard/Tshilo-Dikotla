from collections import OrderedDict

from edc_constants.constants import REQUIRED, NOT_REQUIRED, ADDITIONAL, NOT_ADDITIONAL
from edc_visit_schedule.classes import (
    VisitScheduleConfiguration, site_visit_schedules,
    CrfTuple, MembershipFormTuple, ScheduleTuple, RequisitionPanelTuple)

from tshilo_dikotla.apps.td.constants import INFANT

from ..models import InfantVisit, InfantBirth


class InfantBirthVisitSchedule(VisitScheduleConfiguration):

    name = 'birth visit schedule'
    app_label = 'td_infant'

    membership_forms = OrderedDict({
        'infant_enrollment': MembershipFormTuple('infant_enrollment', InfantBirth, True)})

    schedules = OrderedDict({
        'Infant Enrollment': ScheduleTuple('Infant Enrollment',
                                           'infant_enrollment', None, None)})
    visit_definitions = OrderedDict()
    visit_definitions['2000'] = {
        'title': 'Birth',
        'time_point': 0,
        'base_interval': 0,
        'base_interval_unit': 'D',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': INFANT,
        'visit_tracking_model': InfantVisit,
        'schedule': 'Infant Enrollment',
        'instructions': None,
        'requisitions': (),
        'entries': (
#             CrfTuple(10, u'td_infant', u'infantbirthdata', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(20, u'td_infant', u'infantbirthexam', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(30, u'td_infant', u'infantbirthfeedvaccine', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(40, u'td_infant', u'infantbirtharv', NOT_REQUIRED, ADDITIONAL),
#             CrfTuple(50, u'td_infant', u'infantstoolcollection', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(100, u'td_infant', u'infantcongenitalanomalies', NOT_REQUIRED, ADDITIONAL),
            CrfTuple(200, u'td_infant', u'infantdeathreport', NOT_REQUIRED, ADDITIONAL),
            CrfTuple(230, u'td_infant', u'infantoffstudy', NOT_REQUIRED, ADDITIONAL))}
    visit_definitions['2100'] = {
        'title': 'Infant 1 Month Visit',
        'time_point': 10,
        'base_interval': 1,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': INFANT,
        'visit_tracking_model': InfantVisit,
        'schedule': 'Infant Enrollment',
        'instructions': None,
        'requisitions': (),
        'entries': (
#             CrfTuple(30, u'td_infant', u'infantfu', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(40, u'td_infant', u'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(50, u'td_infant', u'infantfudx', NOT_REQUIRED, ADDITIONAL),
#             CrfTuple(80, u'td_infant', u'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(80, u'td_infant', u'infantfuimmunizations', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(90, u'td_infant', u'infantarvproph', REQUIRED, ADDITIONAL),
#             CrfTuple(100, u'td_infant', u'infantfeeding', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(110, u'td_infant', u'infantstoolcollection', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(200, u'td_infant', u'infantdeathreport', NOT_REQUIRED, ADDITIONAL),
            CrfTuple(240, u'td_infant', u'infantoffstudy', NOT_REQUIRED, ADDITIONAL))}
    visit_definitions['2200'] = {
        'title': 'Infant 2 Month Visit',
        'time_point': 20,
        'base_interval': 2,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': INFANT,
        'visit_tracking_model': InfantVisit,
        'schedule': 'Infant Enrollment',
        'instructions': None,
        'requisitions': (),
        'entries': (
#             CrfTuple(30, u'td_infant', u'infantfu', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(40, u'td_infant', u'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(50, u'td_infant', u'infantfudx', NOT_REQUIRED, ADDITIONAL),
#             CrfTuple(80, u'td_infant', u'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(80, u'td_infant', u'infantfuimmunizations', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(90, u'td_infant', u'infantarvproph', REQUIRED, ADDITIONAL),
#             CrfTuple(100, u'td_infant', u'infantfeeding', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(110, u'td_infant', u'infantstoolcollection', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(110, u'td_infant', u'infantcircumcision', NOT_REQUIRED, ADDITIONAL),
            CrfTuple(200, u'td_infant', u'infantdeathreport', NOT_REQUIRED, ADDITIONAL),
            CrfTuple(240, u'td_infant', u'infantoffstudy', NOT_REQUIRED, ADDITIONAL))}

    visit_definitions['2600'] = {
        'title': 'Infant 6 Month Visit',
        'time_point': 60,
        'base_interval': 6,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': INFANT,
        'visit_tracking_model': InfantVisit,
        'schedule': 'Infant Enrollment',
        'instructions': None,
        'requisitions': (),
        'entries': (
#             CrfTuple(30, u'td_infant', u'infantfu', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(40, u'td_infant', u'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(50, u'td_infant', u'infantfudx', NOT_REQUIRED, ADDITIONAL),
#             CrfTuple(80, u'td_infant', u'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(80, u'td_infant', u'infantfuimmunizations', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(90, u'td_infant', u'infantarvproph', REQUIRED, ADDITIONAL),
#             CrfTuple(100, u'td_infant', u'infantfeeding', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(110, u'td_infant', u'infantstoolcollection', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(110, u'td_infant', u'infantcircumcision', NOT_REQUIRED, ADDITIONAL),
            CrfTuple(200, u'td_infant', u'infantdeathreport', NOT_REQUIRED, ADDITIONAL),
            CrfTuple(240, u'td_infant', u'infantoffstudy', NOT_REQUIRED, ADDITIONAL))}

    visit_definitions['3200'] = {
        'title': 'Infant 12 Month Visit',
        'time_point': 120,
        'base_interval': 12,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': INFANT,
        'visit_tracking_model': InfantVisit,
        'schedule': 'Infant Enrollment',
        'instructions': None,
        'requisitions': (),
        'entries': (
#             CrfTuple(30, u'td_infant', u'infantfu', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(40, u'td_infant', u'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(50, u'td_infant', u'infantfudx', NOT_REQUIRED, ADDITIONAL),
#             CrfTuple(80, u'td_infant', u'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(80, u'td_infant', u'infantfuimmunizations', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(90, u'td_infant', u'infantarvproph', REQUIRED, ADDITIONAL),
#             CrfTuple(100, u'td_infant', u'infantfeeding', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(110, u'td_infant', u'infantstoolcollection', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(200, u'td_infant', u'infantdeathreport', NOT_REQUIRED, ADDITIONAL),
            CrfTuple(240, u'td_infant', u'infantoffstudy', NOT_REQUIRED, ADDITIONAL))}

    visit_definitions['3800'] = {
        'title': 'Infant 18 Month Visit',
        'time_point': 180,
        'base_interval': 18,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': INFANT,
        'visit_tracking_model': InfantVisit,
        'schedule': 'Infant Enrollment',
        'instructions': None,
        'requisitions': (),
        'entries': (
#             CrfTuple(30, u'td_infant', u'infantfu', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(40, u'td_infant', u'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(50, u'td_infant', u'infantfudx', NOT_REQUIRED, ADDITIONAL),
#             CrfTuple(80, u'td_infant', u'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(80, u'td_infant', u'infantfuimmunizations', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(90, u'td_infant', u'infantarvproph', REQUIRED, ADDITIONAL),
#             CrfTuple(100, u'td_infant', u'infantfeeding', REQUIRED, NOT_ADDITIONAL),
#             CrfTuple(110, u'td_infant', u'infantstoolcollection', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(200, u'td_infant', u'infantdeathreport', NOT_REQUIRED, ADDITIONAL),
            CrfTuple(240, u'td_infant', u'infantoffstudy', REQUIRED, ADDITIONAL))}

site_visit_schedules.register(InfantBirthVisitSchedule)
