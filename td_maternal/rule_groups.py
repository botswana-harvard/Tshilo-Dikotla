from edc_constants.constants import YES, UNKEYED, NOT_REQUIRED, POS, NEG, UNK
from edc_rule_groups.classes import RuleGroup, site_rule_groups, Logic, CrfRule, RequisitionRule
from edc_registration.models import RegisteredSubject
from edc_appointment.models import Appointment

from tshilo_dikotla.constants import ONE

from .models import MaternalUltraSoundInitial, MaternalVisit, MaternalPostPartumDep
from .classes import MaternalStatusHelper


def func_mother_pos(visit_instance):
    """Returns true if mother is hiv positive."""
    maternal_status_helper = MaternalStatusHelper(visit_instance)
    if maternal_status_helper.hiv_status == POS:
        return True
    return False


def func_mother_neg(visit_instance):
    """Returns true if mother is hiv neg."""
    maternal_status_helper = MaternalStatusHelper(visit_instance)
    if maternal_status_helper.hiv_status == NEG:
        return True
    return False


def show_rapid_testresult_form(visit_instance):
    """return True if Mother is HIV- and last HIV- result > 3months."""
    maternal_status_helper = MaternalStatusHelper(visit_instance)
    if maternal_status_helper.hiv_status == UNK:
        return True
    return False


def func_require_cd4(visit_instance):
    """Return true if mother is HIV+ and does not have a CD4 in the last 3 months."""
    maternal_status_helper = MaternalStatusHelper(visit_instance)
    if maternal_status_helper.eligible_for_cd4:
        return True
    return False


def show_postpartum_depression(visit_instance):
    """Return true if postpartum depression has to be filled."""
    if (visit_instance.appointment.visit_definition.code != '1200M' and not
        MaternalPostPartumDep.objects.filter(maternal_visit__appointment__visit_definition__code='1200M').exists()):
        return True
    return False


class MaternalRegisteredSubjectRuleGroup(RuleGroup):

    hiv_pos_forms = CrfRule(
        logic=Logic(
            predicate=func_mother_pos,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_maternal', 'maternalrando'),
                      ('td_maternal', 'maternalinterimidcc'),
                      ('td_maternal', 'maternalhivinterimhx'),
                      ('td_maternal', 'maternalarvpreg'),
                      ('td_maternal', 'maternallifetimearvhistory'),
                      ('td_maternal', 'maternalarvpost'),
                      ('td_maternal', 'maternalarvpostadh')])

    rapid_testresult_forms = CrfRule(
        logic=Logic(
            predicate=show_rapid_testresult_form,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_maternal', 'rapidtestresult')])

    post_partumdepression_forms = CrfRule(
        logic=Logic(
            predicate=show_postpartum_depression,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_maternal', 'maternalpostpartumdep')])

#     require_vl = RequisitionRule(
#         logic=Logic(
#             predicate=func_mother_pos,
#             consequence=UNKEYED,
#             alternative=NOT_REQUIRED),
#         target_model=[('td_lab', 'maternalrequisition')],
#         target_requisition_panels=['Viral Load'])
# 
#     require_cd4 = RequisitionRule(
#         logic=Logic(
#             predicate=func_require_cd4,
#             consequence=UNKEYED,
#             alternative=NOT_REQUIRED),
#         target_model=[('td_lab', 'maternalrequisition')],
#         target_requisition_panels=['CD4'])

    class Meta:
        app_label = 'td_maternal'
        source_fk = None
        source_model = RegisteredSubject

site_rule_groups.register(MaternalRegisteredSubjectRuleGroup)


class MaternalUltrasoundInitialRuleGroup(RuleGroup):

    antenatal_enrollment_pass = CrfRule(
        logic=Logic(
            predicate=('number_of_gestations', 'equals', ONE),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_maternal', 'maternalobstericalhistory'),
                      ('td_maternal', 'maternalmedicalhistory'),
                      ('td_maternal', 'maternaldemographics'),
                      ('td_maternal', 'maternallifetimearvhistory'),
                      ('td_maternal', 'maternalarvpreg'),
                      ('td_maternal', 'maternalclinicalmeasurementsone')])

    class Meta:
        app_label = 'td_maternal'
        source_fk = (MaternalVisit, 'maternal_visit')
        source_model = MaternalUltraSoundInitial

site_rule_groups.register(MaternalUltrasoundInitialRuleGroup)