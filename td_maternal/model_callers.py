from edc_call_manager.model_caller import ModelCaller, WEEKLY
from edc_call_manager.decorators import register

from edc_registration.models import RegisteredSubject

from .models import MaternalLocator, MaternalConsent, AntenatalEnrollment, MaternalOffstudy


@register(AntenatalEnrollment, MaternalConsent)
class MaternalModelCaller(ModelCaller):
    label = 'subjects'
    locator_model = (MaternalLocator, 'subject_identifier')
    subject_model = RegisteredSubject
    interval = WEEKLY
    unscheduling_model = MaternalOffstudy
