from edc_call_manager.model_caller import ModelCaller, WEEKLY
from edc_call_manager.decorators import register
from edc_call_manager.models import Call, Log, LogEntry

from td.models import RegisteredSubject

from .models import MaternalLocator, MaternalConsent, AntenatalEnrollment, MaternalOffStudy


@register(AntenatalEnrollment, MaternalOffStudy)
class MaternalModelCaller(ModelCaller):
    call_model = (Call, 'subject_identifier')
    label = 'subjects'
    locator_model = (MaternalLocator, 'subject_identifier')
    consent_model = (MaternalConsent, 'subject_identifier')
    subject_model = RegisteredSubject
    log_entry_model = LogEntry
    log_model = Log
    interval = WEEKLY
    # unscheduling_model = MaternalOffStudy
