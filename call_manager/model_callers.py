from edc_call_manager.model_caller import ModelCaller
from edc_call_manager.decorators import register

from td_maternal.models import PotentialCall, MaternalLocator, MaternalConsent
from call_manager.models import Call, Log, LogEntry


@register(PotentialCall)
class PotentialSubjectModelCaller(ModelCaller):
    call_model = (Call, 'potential_call')
    label = 'subjects'
    locator_model = (MaternalLocator, 'potential_call__subject_identifier')
    log_entry_model = LogEntry
    log_model = Log
    unscheduling_model = MaternalConsent
