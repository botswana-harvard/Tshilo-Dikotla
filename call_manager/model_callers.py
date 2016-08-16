from edc_call_manager.model_caller import ModelCaller, MONTHLY
from edc_call_manager.decorators import register
from edc_appointment.models import Appointment
from call_manager.models import Call, Log, LogEntry

from td_maternal.models import MaternalLocator, MaternalConsent, AntenatalEnrollment
from td_maternal.models.maternal_off_study import MaternalOffStudy


@register(AntenatalEnrollment)
class MaternalModelCaller(ModelCaller):
    call_model = (Call, 'registered_subject')
    label = 'subjects'
    locator_model = (MaternalLocator, 'registered_subject__subject_identifier')
    consent_model = (MaternalConsent, 'registered_subject')
    log_entry_model = LogEntry
    log_model = Log
    interval = MONTHLY
    unscheduling_model = MaternalOffStudy
