from edc_constants.constants import YES, UNKEYED, NOT_REQUIRED
from edc_rule_groups.classes import RuleGroup, site_rule_groups, Logic, CrfRule
from edc_registration.models import RegisteredSubject
from edc_appointment.models import Appointment

from tshilo_dikotla.apps.td.constants import ONE

from .models import MaternalUltraSoundInitial, MaternalVisit


class MaternalUltrasoundInitialRuleGroup(RuleGroup):

    antenatal_enrollment = CrfRule(
        logic=Logic(
            predicate=('number_of_gestations', 'equals', ONE),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=[('td_maternal', 'maternalobstericalhistory'), ('td_maternal', 'maternalmedicalhistory'), ('td_maternal', 'maternaldemographics')])

    class Meta:
        app_label = 'td_maternal'
        source_fk = (MaternalVisit, 'maternal_visit')
        source_model = MaternalUltraSoundInitial

# site_rule_groups.register(MaternalUltrasoundInitialRuleGroup)

