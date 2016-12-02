from dateutil.relativedelta import relativedelta

from edc_constants.constants import POS, NEG, UNK, IND
from edc_metadata.constants import NOT_REQUIRED, REQUIRED
from edc_rule_groups.crf_rule import CrfRule
from edc_rule_groups.decorators import register
from edc_rule_groups.logic import Logic
from edc_rule_groups.predicate import P
from edc_rule_groups.requisition_rule import RequisitionRule
from edc_rule_groups.rule_group import RuleGroup

from td.constants import ONE

from .lab_profiles import cd4_panel, pbmc_vl_panel, pbmc_panel, hiv_elisa_panel
from .maternal_hiv_status import MaternalHivStatus
from .models import (
    MaternalUltraSoundInitial, MaternalPostPartumDep, RapidTestResult, MaternalRando, MaternalInterimIdcc)


def func_mother_pos(visit_instance, *args):
    """Returns true if mother is hiv positive."""
    maternal_hiv_status = MaternalHivStatus(
        subject_identifier=visit_instance.subject_identifier,
        reference_datetime=visit_instance.report_datetime)
    if maternal_hiv_status.result == POS:
        return True
    return False


def func_mother_neg(visit_instance, *args):
    """Returns true if mother is hiv neg."""
    maternal_hiv_status = MaternalHivStatus(
        subject_identifier=visit_instance.subject_identifier,
        reference_datetime=visit_instance.report_datetime)
    if maternal_hiv_status.result == NEG:
        return True
    return False


def show_elisa_requisition_hiv_status_ind(visit_instance, *args):
    """return True if Mother's Rapid Test Result is Inditerminate"""
    maternal_hiv_status = MaternalHivStatus(
        subject_identifier=visit_instance.subject_identifier,
        reference_datetime=visit_instance.report_datetime)
    if maternal_hiv_status.result == IND:
        return True
    return False


def func_require_cd4(visit_instance, *args):
    """Return true if mother is HIV+ and does not have a CD4 in the last 3 months."""
    require_cd4 = False
    maternal_hiv_status = MaternalHivStatus(
        subject_identifier=visit_instance.subject_identifier,
        reference_datetime=visit_instance.report_datetime)
    if not maternal_hiv_status.result == POS:
        try:
            obj = MaternalInterimIdcc.objects.get(maternal_visit=visit_instance)
            if obj.recent_cd4_date:
                if (visit_instance.report_datetime - relativedelta(months=3)).date() > obj.recent_cd4_date:
                    require_cd4 = True
        except MaternalInterimIdcc.DoesNotExist:
            pass
    return require_cd4


def show_postpartum_depression(visit_instance, *args):
    """Return true if postpartum depression has to be filled."""
    if (visit_instance.appointment.visit_code != '2010M' and not
        MaternalPostPartumDep.objects.filter(
            maternal_visit__appointment__visit_code='2010M',
            maternal_visit__appointment=visit_instance.appointment).exists()):
        return True
    return False


def show_ultrasound_form(visit_instance, *args):
    """Return True if ultrasound form has to be filled."""
    show_ultrasound_form = False
    try:
        MaternalUltraSoundInitial.objects.get(maternal_visit__subject_identifier=visit_instance.subject_identifier)
    except MaternalUltraSoundInitial.DoesNotExist:
        if visit_instance.appointment.visit_code in ['1000M', '1010M']:
            show_ultrasound_form = True
    return show_ultrasound_form


def show_rapid_test_form(visit_instance, *args):
    """
        Return true if the the day of the last rapid test is
       (EDD confirmed) (Date of Last HIV Rapid Test) > 56 OR Unknown
    """
    subject_identifier = visit_instance.appointment.subject_identifier
    maternal_hiv_status = MaternalHivStatus(
        subject_identifier=visit_instance.subject_identifier,
        reference_datetime=visit_instance.report_datetime)
    if visit_instance.appointment.visit_code == '2000M':
        if maternal_hiv_status.result == NEG:
            # Get the last date the Rapid Test was processed.
            prev_rapid_test = (RapidTestResult.objects.filter(
                maternal_visit__appointment__subject_identifier=subject_identifier).
                order_by('-created').first())

            # Get the EDD confirmed.
            maternal_ultrasound = (MaternalUltraSoundInitial.objects.filter(
                maternal_visit__appointment__subject_identifier=subject_identifier)
                .order_by('-created').first())
            if prev_rapid_test and maternal_ultrasound:
                if (maternal_ultrasound.edd_confirmed - prev_rapid_test.result_date).days < 56:
                    return False
                if (maternal_ultrasound.edd_confirmed - prev_rapid_test.result_date).days > 56:
                    return True
            else:
                return True
    else:
        if maternal_hiv_status.result == UNK:
            return True
        return False


def func_show_nvp_dispensing_form(visit_instance, *args):
    func_show_nvp_dispensing_form = False
    if func_mother_pos(visit_instance):
        try:
            randomization = MaternalRando.objects.get(
                subject_identifier=visit_instance.appointment.subject_identifier)
            func_show_nvp_dispensing_form = randomization.rx.strip('\n') == 'NVP'
        except MaternalRando.DoesNotExist:
            pass
    return func_show_nvp_dispensing_form


@register()
<<<<<<< HEAD
class MaternalVisitRuleGroup(RuleGroup):
=======
class MaternalRuleGroup(RuleGroup):
>>>>>>> 731ed385345ce31ded9932770f0c860d0bcde079

    require_ultrasound = CrfRule(
        logic=Logic(
            predicate=show_ultrasound_form,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['maternalultrasoundinitial'])

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

    nvp_dispensing_form = CrfRule(
        logic=Logic(
            predicate=func_show_nvp_dispensing_form,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['nvpdispensing'])

    class Meta:
        app_label = 'td_maternal'
        source_model = 'td_maternal.maternalvisit'


@register()
class MaternalRequisitionRuleGroup(RuleGroup):

    require_vl = RequisitionRule(
        logic=Logic(
            predicate=func_mother_pos,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='td_lab.maternalrequisition',
        target_panels=[pbmc_vl_panel])

    require_pbmc_storage = RequisitionRule(
        logic=Logic(
            predicate=func_mother_neg,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='td_lab.maternalrequisition',
        target_panels=[pbmc_panel])

    require_elisa_status_ind = RequisitionRule(
        logic=Logic(
            predicate=show_elisa_requisition_hiv_status_ind,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='td_lab.maternalrequisition',
        target_panels=[hiv_elisa_panel])

    require_elisa = RequisitionRule(
        logic=Logic(
            predicate=func_mother_pos,
            consequence=NOT_REQUIRED,
            alternative=REQUIRED),
        target_model='td_lab.maternalrequisition',
        target_panels=[hiv_elisa_panel])

    class Meta:
        app_label = 'td_maternal'
        source_model = 'edc_registration.registeredsubject'


@register()
class MaternalRequisitionRuleGroupCD4(RuleGroup):

    require_cd4 = RequisitionRule(
        logic=Logic(
            predicate=func_require_cd4,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='td_lab.maternalrequisition',
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
