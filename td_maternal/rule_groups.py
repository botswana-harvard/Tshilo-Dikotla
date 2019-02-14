from edc_appointment.models.appointment import Appointment
from edc_constants.constants import UNKEYED, NOT_REQUIRED, POS, NEG, UNK, IND
from edc_constants.constants import YES
from edc_registration.models import RegisteredSubject
from edc_rule_groups.classes import RuleGroup, site_rule_groups, Logic, CrfRule, RequisitionRule

from td_lab.models import MaternalRequisition
from tshilo_dikotla.constants import ONE

from .classes import MaternalStatusHelper
from .models import MaternalPostPartumDep, RapidTestResult, MaternalInterimIdcc
from .models import MaternalUltraSoundInitial, MaternalVisit, MaternalContraception


def get_previous_visit(visit_instance, timepoints, visit_model):
    registered_subject = visit_instance.appointment.registered_subject
    position = timepoints.index(
        visit_instance.appointment.visit_definition.code)
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


def func_mother_pos(visit_instance):
    """Returns true if mother is hiv positive."""
    maternal_status_helper = MaternalStatusHelper(visit_instance)
    if maternal_status_helper.hiv_status == POS:
        return True
    return False


def require_pbmc_vl(visit_instance):
    if visit_instance.appointment.visit_definition.code in ['2000M', '2010M', '2020M']:
        return False
    else:
        return func_mother_pos(visit_instance) and visit_instance.appointment.visit_instance == '0'


def func_mother_pos_vl(visit_instance):
    if (func_mother_pos(visit_instance) and
            (visit_instance.appointment.visit_definition.code in ['1010M' '1020M', '2120M'
                                                                  '2180M' '2240M'
                                                                  '2300M' '2360M'])):
        return False
    elif (func_mother_pos(visit_instance)
          and visit_instance.appointment.visit_instance == '0'
          and visit_instance.appointment.visit_definition.code in ['2000M', '2010M',
                                                                   '2020M', '2020M',
                                                                   '2060M']):
        return True


def func_mother_neg(visit_instance):
    """Returns true if mother is hiv neg."""
    maternal_status_helper = MaternalStatusHelper(visit_instance)
    if maternal_status_helper.hiv_status == NEG:
        return True
    return False


# def show_rapid_testresult_form(visit_instance):
#     """return True if Mother is HIV- and last HIV- result > 3months."""
#     maternal_status_helper = MaternalStatusHelper(visit_instance)
#     if maternal_status_helper.hiv_status == UNK:
#         return True
#     return False


def show_elisa_requisition_hiv_status_ind(visit_instance):
    """return True if Mother's Rapid Test Result is Inditerminate"""
    maternal_status_helper = MaternalStatusHelper(visit_instance)
    if maternal_status_helper.hiv_status == IND:
        return True
    return False


def func_require_cd4(visit_instance):
    """Return true if mother is HIV+ and does not have a CD4 in the last 3 months."""
    maternal_status_helper = MaternalStatusHelper(visit_instance)
    if (maternal_status_helper.hiv_status == POS
            and visit_instance.appointment.visit_definition.code == '1010M'):
        return maternal_status_helper.eligible_for_cd4
    return False


def show_postpartum_depression(visit_instance):
    """Return true if postpartum depression has to be filled."""
    if (visit_instance.appointment.visit_definition.code != '2010M' and not
        MaternalPostPartumDep.objects.filter(
            maternal_visit__appointment__visit_definition__code='2010M',
            maternal_visit__appointment=visit_instance.appointment).exists()):
        return True
    return False


def show_ultrasound_form(visit_instance):
    """Return true if ultrasound form has to be filled."""
    if (visit_instance.appointment.visit_definition.code == '1000M'):
        return True
    elif (visit_instance.appointment.visit_definition.code == '1010M' and not
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

    if visit_instance.appointment.visit_definition.code == '2000M':
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


def func_show_srh_services_utilization(visit_instance):
    """Returns True if participant was referred to shr in the last visit."""
    previous_visit = get_previous_visit(visit_instance,
                                        ['1000M', '1010M', '1020M', '2000M', '2010M',
                                         '2020M', '2060M', '2120M', '2180M', '2240M',
                                         '2300M', '2360M'],
                                        MaternalVisit)
    if not previous_visit:
        return False
    try:
        rep_health_refferal = MaternalContraception.objects.get(
            maternal_visit=previous_visit)
        return rep_health_refferal.srh_referral == YES
    except MaternalContraception.DoesNotExist:
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
            predicate=show_rapid_test_form,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_maternal', 'rapidtestresult')])

    post_partumdepression_forms = CrfRule(
        logic=Logic(
            predicate=show_postpartum_depression,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_maternal', 'maternalpostpartumdep')])

    require_ultrasound = CrfRule(
        logic=Logic(
            predicate=show_ultrasound_form,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_maternal', 'maternalultrasoundinitial')])

    srh_services = CrfRule(
        logic=Logic(
            predicate=func_show_srh_services_utilization,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_maternal', 'maternalsrh')])

    class Meta:
        app_label = 'td_maternal'
        source_fk = None
        source_model = RegisteredSubject


site_rule_groups.register(MaternalRegisteredSubjectRuleGroup)


class MaternalRequisitionRuleGroup(RuleGroup):

    require_vl_prn = RequisitionRule(
        logic=Logic(
            predicate=func_mother_pos_vl,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_lab', 'maternalrequisition')],
        target_requisition_panels=['Viral Load'])

    require_pbmc_vl = RequisitionRule(
        logic=Logic(
            predicate=require_pbmc_vl,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_lab', 'maternalrequisition')],
        target_requisition_panels=['PBMC VL'])

    require_pbmc_storage = RequisitionRule(
        logic=Logic(
            predicate=func_mother_neg,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_lab', 'maternalrequisition')],
        target_requisition_panels=['PBMC Plasma (STORE ONLY)'])

    require_elisa_status_ind = RequisitionRule(
        logic=Logic(
            predicate=show_elisa_requisition_hiv_status_ind,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_lab', 'maternalrequisition')],
        target_requisition_panels=['ELISA'])

    require_elisa = RequisitionRule(
        logic=Logic(
            predicate=func_mother_pos,
            consequence=NOT_REQUIRED,
            alternative=UNKEYED),
        target_model=[('td_lab', 'maternalrequisition')],
        target_requisition_panels=['ELISA'])

    class Meta:
        app_label = 'td_maternal'
        source_fk = None
        source_model = RegisteredSubject


site_rule_groups.register(MaternalRequisitionRuleGroup)


class MaternalRequisitionRuleGroupCD4(RuleGroup):

    require_cd4 = RequisitionRule(
        logic=Logic(
            predicate=func_require_cd4,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_lab', 'maternalrequisition')],
        target_requisition_panels=['CD4'])

    class Meta:
        app_label = 'td_maternal'
        source_fk = (MaternalVisit, 'maternal_visit')
        source_model = MaternalInterimIdcc


site_rule_groups.register(MaternalRequisitionRuleGroupCD4)


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
