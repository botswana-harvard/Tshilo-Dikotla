from edc_base.model.models import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_visit_schedule.model_mixins import DisenrollmentModelMixin

from ..managers import InfantDisenrollmentManager


class InfantDisenrollment(DisenrollmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    objects = InfantDisenrollmentManager()

    class Meta(DisenrollmentModelMixin.Meta):
        visit_schedule_name = 'infant_visit_schedule'
        app_label = 'td_infant'
