from edc_appointment.models import Appointment
from edc_constants.constants import YES, NOT_REQUIRED, REQUIRED
from edc_rule_groups.crf_rule import CrfRule
from edc_rule_groups.decorators import register
from edc_rule_groups.logic import Logic
from edc_rule_groups.predicate import P
from edc_rule_groups.requisition_rule import RequisitionRule
from edc_rule_groups.rule_group import RuleGroup

from tshilo_dikotla.constants import NO_MODIFICATIONS, START, MODIFIED
from tshilo_dikotla.td_infant_lab_profiles import (infant_pp1_heu_pbmc_pl_panel,
                                                   infant_pp1_huu_pbmc_pl_panel, infant_heelstick_panel,
                                                   infant_pp18_heu_insulin_panel, infant_pp18_huu_insulin_panel)

from td_maternal.rule_groups import func_mother_pos
from td_maternal.models import MaternalVisit

from td_registration.models import RegisteredSubject

from td_infant.models import InfantArvProph, InfantVisit, InfantFu, InfantBirthData, InfantFeeding


def get_previous_visit(visit_instance, timepoints, visit_model):
    registered_subject = visit_instance.appointment.registered_subject
    position = timepoints.index(visit_instance.appointment.visit_definition.code)
    timepoints_slice = timepoints[:position]
    if len(timepoints_slice) > 1:
        timepoints_slice.reverse()
    for point in timepoints_slice:
        try:
            previous_appointment = Appointment.objects.filter(
                registered_subject=registered_subject, visit_definition__code=point).order_by('-created').first()
            return visit_model.objects.filter(appointment=previous_appointment).order_by('-created').first()
        except Appointment.DoesNotExist:
            pass
        except visit_model.DoesNotExist:
            pass
        except AttributeError:
            pass
    return None


def maternal_hiv_status_visit(visit_instance):
    maternal_registered_subject = RegisteredSubject.objects.get(
        subject_identifier=visit_instance.appointment.registered_subject.relative_identifier)
    try:
        maternal_visit_2000 = MaternalVisit.objects.get(
            subject_identifier=maternal_registered_subject.subject_identifier,
            appointment__visit_definition__code='2000M')
        return func_mother_pos(maternal_visit_2000)
    except Exception:
        pass


def func_show_infant_arv_proph(visit_instance):
    previous_visit = get_previous_visit(visit_instance,
                                        ['2000', '2010', '2020', '2060', '2090', '2120', '2180', '2240', '2300',
                                         '2360'],
                                        InfantVisit)
    if not previous_visit:
        return False
    try:
        infant_arv_proph = InfantArvProph.objects.get(infant_visit=previous_visit)
        return infant_arv_proph.arv_status in [NO_MODIFICATIONS, START, MODIFIED]
    except InfantArvProph.DoesNotExist:
        if visit_instance.appointment.visit_definition.code == '2010':
            return maternal_hiv_status_visit(visit_instance)
        return False


def func_infant_heu(visit_instance):
    """Returns true if mother of the infant is hiv positive."""
    appointment = visit_instance.appointment
    maternal_visit = MaternalVisit.objects.filter(
        appointment__registered_subject__subject_identifier=appointment.registered_subject.relative_identifier
    ).order_by('-created').first()
    if func_mother_pos(maternal_visit):
        return True
    return False


@register()
class InfantFuRuleGroup(RuleGroup):

    physical_assessment_yes = CrfRule(
        logic=Logic(
            predicate=('physical_assessment', 'equals', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model=['infantfuphysical'])

    has_dx_yes = CrfRule(
        logic=Logic(
            predicate=('has_dx', 'equals', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model=['infantfudx'])

    class Meta:
        app_label = 'td_infant'
        source_model = 'td_infant.infantfu'


@register()
class InfantFeedingRuleGroup(RuleGroup):

    solid_foods = CrfRule(
        logic=Logic(
            predicate=('formula_intro_occur', 'equals', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model=['solidfoodassessment'])

    class Meta:
        app_label = 'td_infant'
        source_model = 'td_infant.infantfeeding'


@register()
class InfantBirthDataRuleGroup(RuleGroup):

    congenital_anomalities_yes = CrfRule(
        logic=Logic(
            predicate=('congenital_anomalities', 'equals', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model=['infantcongenitalanomalies'])

    class Meta:
        app_label = 'td_infant'
        source_model = 'td_infant.infantbirthdata'


@register()
class InfantRequisitionRuleGroup(RuleGroup):

    require_pbmc_pl_heu_pp1 = RequisitionRule(
        logic=Logic(
            predicate=func_infant_heu,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model=['infantrequisition'],
        target_requisition_panels=[infant_pp1_heu_pbmc_pl_panel])

    require_pbmc_pl_huu_pp1 = RequisitionRule(
        logic=Logic(
            predicate=not func_infant_heu,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model=['infantrequisition'],
        target_requisition_panels=[infant_pp1_huu_pbmc_pl_panel])

    require_heel_stick = RequisitionRule(
        logic=Logic(
            predicate=func_infant_heu,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model=['infantrequisition'],
        target_requisition_panels=[infant_heelstick_panel])

    require_insulin_heu_pp18 = RequisitionRule(
        logic=Logic(
            predicate=func_infant_heu,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model=['infantrequisition'],
        target_requisition_panels=[infant_pp18_heu_insulin_panel])

    require_insulin_huu_pp18 = RequisitionRule(
        logic=Logic(
            predicate=not func_infant_heu,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model=['infantrequisition'],
        target_requisition_panels=[infant_pp18_huu_insulin_panel])

    class Meta:
        app_label = 'td_infant'
        source_model = 'td_registration.registeredsubject'
