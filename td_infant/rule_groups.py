from edc_constants.constants import YES, NOT_REQUIRED, UNKEYED, POS
from edc_registration.models import RegisteredSubject
from edc_rule_groups.classes import RuleGroup, site_rule_groups, Logic, CrfRule, RequisitionRule

from td_maternal.rule_groups import func_mother_pos
from td_maternal.models import MaternalVisit

from .models import InfantVisit, InfantFu, InfantBirthData

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

def func_check_infant_heu(visit_instance):
    maternal_registered_subject = RegisteredSubject.objects.get(
        subject_identifier=visit_instance.appointment.registered_subject.relative_identifier)
    try:
        maternal_visit_2000 = MaternalVisit.objects.get(
                subject_identifier=maternal_registered_subject, appointment__visit_definition__code='2000M')
        maternal_hiv = func_mother_pos(maternal_visit_2000)
    except:
        return False
    return maternal_hiv == POS


class InfantFuRuleGroup(RuleGroup):

    physical_assessment_yes = CrfRule(
        logic=Logic(
            predicate=('physical_assessment', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_infant', 'infantfuphysical'),])

    has_dx_yes = CrfRule(
        logic=Logic(
            predicate=('has_dx', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_infant', 'infantfudx'),])

    class Meta:
        app_label = 'td_infant'
        source_fk = (InfantVisit, 'infant_visit')
        source_model = InfantFu

site_rule_groups.register(InfantFuRuleGroup)


class InfantBirthDataRuleGroup(RuleGroup):

    congenital_anomalities_yes = CrfRule(
        logic=Logic(
            predicate=('congenital_anomalities', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_infant', 'infantcongenitalanomalies'),])

    class Meta:
        app_label = 'td_infant'
        source_fk = (InfantVisit, 'infant_visit')
        source_model = InfantBirthData

site_rule_groups.register(InfantBirthDataRuleGroup)


class InfantRegisteredSubjectRuleGroup(RuleGroup):

    arv_proph = CrfRule(
        logic=Logic(predicate=func_check_infant_heu,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_infant', 'infantarvproph'),])

    class Meta:
        app_label = 'td_infant'
        source_fk = None
        source_model = RegisteredSubject

site_rule_groups.register(InfantRegisteredSubjectRuleGroup)
