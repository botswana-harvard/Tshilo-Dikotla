from edc_appointment.models import Appointment
from edc_constants.constants import YES, NOT_REQUIRED, UNKEYED
from edc_registration.models import RegisteredSubject
from edc_rule_groups.classes import RuleGroup, site_rule_groups, Logic, CrfRule, RequisitionRule

from tshilo_dikotla.constants import NO_MODIFICATIONS, START, MODIFIED
from td_maternal.rule_groups import func_mother_pos
from td_maternal.models import MaternalVisit

from .models import InfantArvProph

from .models import InfantVisit, InfantFu, InfantBirthData, InfantFeeding


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
    except Exception as e:
        pass


def func_show_infant_arv_proph(visit_instance):
    previous_visit = get_previous_visit(visit_instance,
                                        ['2000', '2010', '2020', '2060', '2090', '2120', '2180', '2240', '2300', '2360'],
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
    latest_maternal_visit = MaternalVisit.objects.filter(
        appointment__registered_subject__subject_identifier=appointment.registered_subject.relative_identifier,
    ).order_by('-created').first()
    if func_mother_pos(latest_maternal_visit):
        return True
    return False


class InfantRegisteredSubjectRuleGroup(RuleGroup):

    arv_proph = CrfRule(
        logic=Logic(
            predicate=func_show_infant_arv_proph,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_infant', 'infantarvproph'), ])

    birth_arv = CrfRule(
        logic=Logic(
            predicate=func_infant_heu,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_infant', 'infantbirtharv'), ])

    class Meta:
        app_label = 'td_infant'
        source_fk = None
        source_model = RegisteredSubject
site_rule_groups.register(InfantRegisteredSubjectRuleGroup)


class InfantFuRuleGroup(RuleGroup):

    physical_assessment_yes = CrfRule(
        logic=Logic(
            predicate=('physical_assessment', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_infant', 'infantfuphysical'), ])

    has_dx_yes = CrfRule(
        logic=Logic(
            predicate=('has_dx', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_infant', 'infantfudx'), ])

    class Meta:
        app_label = 'td_infant'
        source_fk = (InfantVisit, 'infant_visit')
        source_model = InfantFu

site_rule_groups.register(InfantFuRuleGroup)


class InfantFeedingRuleGroup(RuleGroup):

    solid_foods = CrfRule(
        logic=Logic(
            predicate=('formula_intro_occur', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_infant', 'solidfoodassessment'), ])

    class Meta:
        app_label = 'td_infant'
        source_fk = (InfantVisit, 'infant_visit')
        source_model = InfantFeeding

site_rule_groups.register(InfantFeedingRuleGroup)


class InfantBirthDataRuleGroup(RuleGroup):

    congenital_anomalities_yes = CrfRule(
        logic=Logic(
            predicate=('congenital_anomalities', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_infant', 'infantcongenitalanomalies'), ])

    class Meta:
        app_label = 'td_infant'
        source_fk = (InfantVisit, 'infant_visit')
        source_model = InfantBirthData

site_rule_groups.register(InfantBirthDataRuleGroup)


class InfantRequisitionRuleGroup(RuleGroup):

    require_dna_pcr = RequisitionRule(
        logic=Logic(
            predicate=func_infant_heu,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_lab', 'infantrequisition')],
        target_requisition_panels=['DNA PCR'])

    require_dbs = RequisitionRule(
        logic=Logic(
            predicate=func_infant_heu,
            consequence=NOT_REQUIRED,
            alternative=UNKEYED),
        target_model=[('td_lab', 'infantrequisition')],
        target_requisition_panels=['DBS (Store Only)'])

#     require_plasma_pbmc = RequisitionRule(
#         logic=Logic(
#             predicate=func_plasma_pbmc,
#             consequence=UNKEYED,
#             alternative=NOT_REQUIRED),
#         target_model=[('td_lab', 'maternalrequisition')],
#         target_requisition_panels=['PBMC Plasma (STORE ONLY)'])
# 
#     require_insulin_glucose = RequisitionRule(
#         logic=Logic(
#             predicate=func_insulin_glucose,
#             consequence=UNKEYED,
#             alternative=NOT_REQUIRED),
#         target_model=[('td_lab', 'maternalrequisition')],
#         target_requisition_panels=['Infant Insulin', 'Infant Glucose'])

    class Meta:
        app_label = 'td_infant'
        source_fk = None
        source_model = RegisteredSubject

site_rule_groups.register(InfantRequisitionRuleGroup)
