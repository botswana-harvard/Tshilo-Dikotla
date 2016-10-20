from collections import OrderedDict

from edc_constants.constants import REQUIRED, NOT_REQUIRED, ADDITIONAL, NOT_ADDITIONAL
from edc_visit_schedule.classes import (
    VisitScheduleConfiguration, site_visit_schedules,
    CrfTuple, MembershipFormTuple, ScheduleTuple, RequisitionPanelTuple)

from tshilo_dikotla.constants import INFANT

from ..models import InfantVisit, InfantBirth


class InfantBirthVisitSchedule(VisitScheduleConfiguration):

    name = 'birth visit schedule'
    app_label = 'td_infant'

    membership_forms = OrderedDict({
        'infant_enrollment': MembershipFormTuple('infant_enrollment', InfantBirth, True)})

    schedules = OrderedDict({
        'Infant Enrollment': ScheduleTuple('Infant Enrollment',
                                           'infant_enrollment', None, None)})

    infant_birth_requisitions = (
        RequisitionPanelTuple(
            10, 'td_lab', 'infantrequisition',
            'Infant Insulin', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL),
        RequisitionPanelTuple(
            20, 'td_lab', 'infantrequisition',
            'Infant Serum (Store Only)', 'STORAGE', 'WB', REQUIRED, NOT_ADDITIONAL),
        RequisitionPanelTuple(
            30, 'td_lab', 'infantrequisition',
            'Infant Glucose', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL),
        RequisitionPanelTuple(
            40, 'td_lab', 'infantrequisition',
            'Infant PBMC PL', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL)
    )

    infant_1month_requisitions = (
        RequisitionPanelTuple(
            10, 'td_lab', 'infantrequisition',
            'Infant Insulin', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL),
        RequisitionPanelTuple(
            20, 'td_lab', 'infantrequisition',
            'Infant Glucose', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL),
        RequisitionPanelTuple(
            30, 'td_lab', 'infantrequisition',
            'DNA PCR', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL),
        RequisitionPanelTuple(
            40, 'td_lab', 'infantrequisition',
            'PBMC Plasma (STORE ONLY)', 'STORAGE', 'WB', REQUIRED, NOT_ADDITIONAL)
    )

    infant_dnapcr_requisitions = (
        RequisitionPanelTuple(
            10, 'td_lab', 'infantrequisition',
            'DNA PCR', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL),
    )

    infant_36month_requisitions = (
        RequisitionPanelTuple(
            10, 'td_lab', 'infantrequisition',
            'Infant Insulin', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL),
        RequisitionPanelTuple(
            20, 'td_lab', 'infantrequisition',
            'Infant Glucose', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL),
        RequisitionPanelTuple(
            30, 'td_lab', 'infantrequisition',
            'PBMC Plasma (STORE ONLY)', 'STORAGE', 'WB', REQUIRED, NOT_ADDITIONAL)
    )

    infant_18month_requisitions = (
        RequisitionPanelTuple(
            10, 'td_lab', 'infantrequisition',
            'Infant Insulin', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL),
        RequisitionPanelTuple(
            20, 'td_lab', 'infantrequisition',
            'Infant Glucose', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL),
        RequisitionPanelTuple(
            40, 'td_lab', 'infantrequisition',
            'ELISA', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL)
    )

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
        'requisitions': infant_birth_requisitions,
        'entries': (
            CrfTuple(10, 'td_infant', 'infantbirthdata', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(20, 'td_infant', 'infantbirthexam', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(30, 'td_infant', 'infantbirthfeedingvaccine', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(40, 'td_infant', 'infantbirtharv', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(50, 'td_infant', 'infantcongenitalanomalies', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(60, 'td_infant', 'infantdeathreport', NOT_REQUIRED, ADDITIONAL))}
    visit_definitions['2010'] = {
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
        'requisitions': infant_1month_requisitions,
        'entries': (
            CrfTuple(10, 'td_infant', 'infantfu', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(20, 'td_infant', 'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(30, 'td_infant', 'infantfudx', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(40, 'td_infant', 'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(50, 'td_infant', 'infantarvproph', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(60, 'td_infant', 'infantfeeding', REQUIRED, NOT_ADDITIONAL))}
    visit_definitions['2020'] = {
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
        'requisitions': infant_dnapcr_requisitions,
        'entries': (
            CrfTuple(10, 'td_infant', 'infantfu', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(20, 'td_infant', 'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(30, 'td_infant', 'infantfudx', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(40, 'td_infant', 'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(40, 'td_infant', 'infantfuimmunizations', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(50, 'td_infant', 'infantarvproph', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(60, 'td_infant', 'infantfeeding', REQUIRED, NOT_ADDITIONAL))}

    visit_definitions['2060'] = {
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
        'requisitions': infant_dnapcr_requisitions,
        'entries': (
            CrfTuple(10, 'td_infant', 'infantfu', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(20, 'td_infant', 'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(30, 'td_infant', 'infantfudx', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(40, 'td_infant', 'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(50, 'td_infant', 'infantarvproph', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(60, 'td_infant', 'infantfeeding', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(70, 'td_infant', 'solidfoodassessment', REQUIRED, NOT_ADDITIONAL))}

    visit_definitions['2120'] = {
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
        'requisitions': infant_dnapcr_requisitions,
        'entries': (
            CrfTuple(10, 'td_infant', 'infantfu', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(20, 'td_infant', 'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(30, 'td_infant', 'infantfudx', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(40, 'td_infant', 'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(50, 'td_infant', 'infantarvproph', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(60, 'td_infant', 'infantfeeding', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(70, 'td_infant', 'solidfoodassessment', REQUIRED, NOT_ADDITIONAL))}

    visit_definitions['2180'] = {
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
        'requisitions': infant_18month_requisitions,
        'entries': (
            CrfTuple(10, 'td_infant', 'infantfu', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(20, 'td_infant', 'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(30, 'td_infant', 'infantfudx', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(40, 'td_infant', 'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(50, 'td_infant', 'infantarvproph', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(60, 'td_infant', 'infantfeeding', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(70, 'td_infant', 'solidfoodassessment', REQUIRED, NOT_ADDITIONAL))}

    visit_definitions['2240'] = {
        'title': 'Infant 24 Month Visit',
        'time_point': 240,
        'base_interval': 24,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': INFANT,
        'visit_tracking_model': InfantVisit,
        'schedule': 'Infant Enrollment',
        'instructions': None,
        'requisitions': infant_dnapcr_requisitions,
        'entries': (
            CrfTuple(10, 'td_infant', 'infantfu', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(20, 'td_infant', 'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(30, 'td_infant', 'infantfudx', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(40, 'td_infant', 'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(50, 'td_infant', 'infantarvproph', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(60, 'td_infant', 'infantfeeding', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(70, 'td_infant', 'solidfoodassessment', REQUIRED, NOT_ADDITIONAL))}

    visit_definitions['2300'] = {
        'title': 'Infant 30 Month Visit',
        'time_point': 300,
        'base_interval': 30,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': INFANT,
        'visit_tracking_model': InfantVisit,
        'schedule': 'Infant Enrollment',
        'instructions': None,
        'requisitions': infant_dnapcr_requisitions,
        'entries': (
            CrfTuple(10, 'td_infant', 'infantfu', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(20, 'td_infant', 'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(30, 'td_infant', 'infantfudx', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(40, 'td_infant', 'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(50, 'td_infant', 'infantarvproph', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(60, 'td_infant', 'infantfeeding', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(70, 'td_infant', 'solidfoodassessment', REQUIRED, NOT_ADDITIONAL))}

    visit_definitions['2360'] = {
        'title': 'Infant 36 Month Visit',
        'time_point': 360,
        'base_interval': 36,
        'base_interval_unit': 'M',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': INFANT,
        'visit_tracking_model': InfantVisit,
        'schedule': 'Infant Enrollment',
        'instructions': None,
        'requisitions': infant_36month_requisitions,
        'entries': (
            CrfTuple(10, 'td_infant', 'infantfu', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(20, 'td_infant', 'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(30, 'td_infant', 'infantfudx', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(40, 'td_infant', 'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(50, 'td_infant', 'infantarvproph', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(60, 'td_infant', 'infantfeeding', REQUIRED, NOT_ADDITIONAL),
            CrfTuple(70, 'td_infant', 'solidfoodassessment', REQUIRED, NOT_ADDITIONAL))}

site_visit_schedules.register(InfantBirthVisitSchedule)
