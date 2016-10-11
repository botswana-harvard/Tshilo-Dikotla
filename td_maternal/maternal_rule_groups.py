from edc_metadata.constants import NOT_REQUIRED, REQUIRED
from edc_constants.constants import POS, NEG, UNK, IND
from edc_rule_groups.crf_rule import CrfRule
from edc_rule_groups.decorators import register
from edc_rule_groups.logic import Logic
from edc_rule_groups.predicate import P
from edc_rule_groups.requisition_rule import RequisitionRule
from edc_rule_groups.rule_group import RuleGroup

from tshilo_dikotla.constants import ONE
from .td_maternal_lab_profiles import (cd4_panel, pbmc_vl_panel, pbmc_panel, hiv_elisa_panel)

from td_maternal.classes import MaternalStatusHelper
from td_maternal.models import MaternalUltraSoundInitial, MaternalPostPartumDep, RapidTestResult


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


def show_elisa_requisition_hiv_status_ind(visit_instance):
    """return True if Mother's Rapid Test Result is Inditerminate"""
    maternal_status_helper = MaternalStatusHelper(visit_instance)
    if maternal_status_helper.hiv_status == IND:
        return True
    return False


def func_require_cd4(visit_instance):
    """Return true if mother is HIV+ and does not have a CD4 in the last 3 months."""
    maternal_status_helper = MaternalStatusHelper(visit_instance)
    if maternal_status_helper.hiv_status == POS:
        return maternal_status_helper.eligible_for_cd4
    return False


def show_postpartum_depression(visit_instance):
    """Return true if postpartum depression has to be filled."""
    if (visit_instance.appointment.visit_code != '2010M' and not
        MaternalPostPartumDep.objects.filter(
            maternal_visit__appointment__visit_definition__code='2010M',
            maternal_visit__appointment=visit_instance.appointment).exists()):
        return True
    return False


def show_ultrasound_form(visit_instance):
    """Return true if ultrasound form has to be filled."""
    if (visit_instance.appointment.visit_code == '1000M'):
        return True
    elif (visit_instance.appointment.visit_code == '1010M' and not
          MaternalUltraSoundInitial.objects.filter(
            maternal_visit__appointment__visit_definition__code='1000M').exists()):
        return True
    return False


def show_rapid_test_form(visit_instance):
    """
        Return true if the the day of the last rapid test is
       (EDD confirmed) – (Date of Last HIV Rapid Test) > 56 OR Unknown
    """
    subject_identifier = visit_instance.appointment.registered_subject.subject_identifier
    maternal_status_helper = MaternalStatusHelper(visit_instance)

    if visit_instance.appointment.visit_code == '2000M':
        if maternal_status_helper.hiv_status == NEG:
            # Get the last date the Rapid Test was processed.
            prev_rapid_test = (RapidTestResult.objects.filter(
                maternal_visit__appointment__registered_subject__subject_identifier=subject_identifier).
                order_by('-created').first())

            # Get the EDD confirmed.
            maternal_ultrasound = (MaternalUltraSoundInitial.objects.filter(
                maternal_visit__appointment__registered_subject__subject_identifier=subject_identifier)
                .order_by('-created').first())
            if prev_rapid_test and maternal_ultrasound:
                if (maternal_ultrasound.edd_confirmed - prev_rapid_test.result_date).days < 56:
                    return False
                if (maternal_ultrasound.edd_confirmed - prev_rapid_test.result_date).days > 56:
                    return True
            else:
                return True
    else:
        if maternal_status_helper.hiv_status == UNK:
            return True
        return False


@register()
class MaternalRegisteredSubjectRuleGroup(RuleGroup):

    hiv_pos_forms = CrfRule(
        logic=Logic(
            predicate=func_mother_pos,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['maternalrando', 'maternalinterimidcc', 'maternalhivinterimhx', 'maternalaztnvp',
                       'maternalarvpreg', 'maternallifetimearvhistory', 'maternalarvpost', 'maternalarvpostadh'])

    rapid_testresult_forms = CrfRule(
        logic=Logic(
            predicate=show_rapid_test_form,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['rapidtestresult'])

    post_partumdepression_forms = CrfRule(
        logic=Logic(
            predicate=show_postpartum_depression,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['maternalpostpartumdep'])

    require_ultrasound = CrfRule(
        logic=Logic(
            predicate=show_ultrasound_form,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['maternalultrasoundinitial'])

    class Meta:
        app_label = 'td_maternal'
        #source_model = 'td_registration.registeredsubject'


@register()
class MaternalRequisitionRuleGroup(RuleGroup):

    require_vl = RequisitionRule(
        logic=Logic(
            predicate=func_mother_pos,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='maternalrequisition',
        target_panels=[pbmc_vl_panel])

    require_pbmc_storage = RequisitionRule(
        logic=Logic(
            predicate=func_mother_neg,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='maternalrequisition',
        target_panels=[pbmc_panel])

    require_elisa_status_ind = RequisitionRule(
        logic=Logic(
            predicate=show_elisa_requisition_hiv_status_ind,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='maternalrequisition',
        target_panels=[hiv_elisa_panel])

    require_elisa = RequisitionRule(
        logic=Logic(
            predicate=func_mother_pos,
            consequence=NOT_REQUIRED,
            alternative=REQUIRED),
        target_model='maternalrequisition',
        target_panels=[hiv_elisa_panel])

    class Meta:
        app_label = 'td_maternal'
        source_model = 'td_registration.registeredsubject'


@register()
class MaternalRequisitionRuleGroupCD4(RuleGroup):

    require_cd4 = RequisitionRule(
        logic=Logic(
            predicate=func_require_cd4,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='maternalrequisition',
        target_panels=[cd4_panel])

    class Meta:
        app_label = 'td_maternal'
        source_model = 'td_maternal.maternalinterimidcc'


@register()
class MaternalUltrasoundInitialRuleGroup(RuleGroup):

    antenatal_enrollment_pass = CrfRule(
        logic=Logic(
            predicate=P('number_of_gestations', 'equals', ONE),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['maternalobstericalhistory', 'maternalmedicalhistory', 'maternaldemographics',
                      'maternallifetimearvhistory', 'maternalarvpreg', 'maternalclinicalmeasurementsone'])

    class Meta:
        app_label = 'td_maternal'
        source_model = 'td_maternal.maternalultrasoundinitial'
