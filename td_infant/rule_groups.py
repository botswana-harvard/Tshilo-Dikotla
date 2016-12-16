from edc_constants.constants import YES
from edc_metadata.constants import NOT_REQUIRED, REQUIRED
from edc_rule_groups.crf_rule import CrfRule
from edc_rule_groups.decorators import register
from edc_rule_groups.logic import Logic
from edc_rule_groups.predicate import P
from edc_rule_groups.requisition_rule import RequisitionRule
from edc_rule_groups.rule_group import RuleGroup
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from edc_registration.models import RegisteredSubject
from td_maternal.models import MaternalVisit
from td_maternal.rule_groups import func_mother_pos
from td.constants import NO_MODIFICATIONS, START, MODIFIED

from .lab_profiles import (
    infant_pp1_heu_pbmc_pl_panel, infant_pp1_huu_pbmc_pl_panel, infant_heelstick_panel,
    infant_pp18_heu_insulin_panel, infant_pp18_huu_insulin_panel)
from .models import InfantArvProph


def func_infant_is_heu(infant_visit, *args):
    """Returns True infant is HIV NEG and mother is HIV POS."""
    # TODO: what is status of infant, if HEU is NEG?? Should this be verified?
    maternal_identifier = RegisteredSubject.objects.get(
        subject_identifier=infant_visit.appointment.subject_identifier).relative_identifier
    maternal_visit = MaternalVisit.objects.filter(
        appointment__subject_identifier=maternal_identifier).order_by('-created').first()
    return func_mother_pos(maternal_visit)


def func_show_infant_arv_proph(infant_visit, *args):
    show_infant_arv_proph = False
    infant_birth_schedule = site_visit_schedules.get_visit_schedule(
        'infant_visit_schedule').schedules.get('infant_birth')
    previous_visit = infant_birth_schedule.get_previous_visit(infant_visit.appointment.visit_code)
    if previous_visit:
        try:
            infant_arv_proph = InfantArvProph.objects.get(
                infant_visit__appointment__visit_code=previous_visit.code)
            show_infant_arv_proph = infant_arv_proph.arv_status in [NO_MODIFICATIONS, START, MODIFIED]
        except InfantArvProph.DoesNotExist:
            if infant_visit.appointment.visit_code == '2010':
                # always show at 2010 if HEU
                show_infant_arv_proph = func_infant_is_heu(infant_visit)
    return show_infant_arv_proph


@register()
class InfantVisitRuleGroup(RuleGroup):

    arv_proph = CrfRule(
        logic=Logic(
            predicate=func_show_infant_arv_proph,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['infantarvproph'])

    class Meta:
        app_label = 'td_infant'
        source_model = 'td_infant.infantvisit'


@register()
class InfantFuRuleGroup(RuleGroup):

    physical_assessment_yes = CrfRule(
        logic=Logic(
            predicate=P('physical_assessment', 'eq', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['infantfuphysical'])

    has_dx_yes = CrfRule(
        logic=Logic(
            predicate=P('has_dx', 'eq', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['infantfudx'])

    class Meta:
        app_label = 'td_infant'
        source_model = 'td_infant.infantfu'


@register()
class InfantFeedingRuleGroup(RuleGroup):

    solid_foods = CrfRule(
        logic=Logic(
            predicate=P('formula_intro_occur', 'eq', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['solidfoodassessment'])

    class Meta:
        app_label = 'td_infant'
        source_model = 'td_infant.infantfeeding'


@register()
class InfantBirthDataRuleGroup(RuleGroup):

    congenital_anomalities_yes = CrfRule(
        logic=Logic(
            predicate=P('congenital_anomalities', 'eq', 'Yes'),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['infantcongenitalanomalies'])

    class Meta:
        app_label = 'td_infant'
        source_model = 'td_infant.infantbirthdata'


@register()
class InfantRequisitionRuleGroup(RuleGroup):

    require_pbmc_pl_heu_pp1 = RequisitionRule(
        logic=Logic(
            predicate=func_infant_is_heu,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='infantrequisition',
        target_panels=[infant_pp1_heu_pbmc_pl_panel])

    require_pbmc_pl_huu_pp1 = RequisitionRule(
        logic=Logic(
            predicate=func_infant_is_heu,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='infantrequisition',
        target_panels=[infant_pp1_huu_pbmc_pl_panel])

    require_heel_stick = RequisitionRule(
        logic=Logic(
            predicate=func_infant_is_heu,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='infantrequisition',
        target_panels=[infant_heelstick_panel])

    require_insulin_heu_pp18 = RequisitionRule(
        logic=Logic(
            predicate=func_infant_is_heu,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='infantrequisition',
        target_panels=[infant_pp18_heu_insulin_panel])

    require_insulin_huu_pp18 = RequisitionRule(
        logic=Logic(
            predicate=func_infant_is_heu,  # TODO: Result must be false
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='infantrequisition',
        target_panels=[infant_pp18_huu_insulin_panel])

    class Meta:
        app_label = 'td_lab'
        source_model = 'td_infant.infantvisit'
