from edc_base.model.models import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_visit_schedule.model_mixins import DisenrollmentModelMixin

from ..managers import MaternalDisenrollmentManager


class MaternalDisenrollment(DisenrollmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'td_maternal_admin'

    objects = MaternalDisenrollmentManager()

    class Meta(DisenrollmentModelMixin.Meta):
        visit_schedule_name = 'maternal_visit_schedule'
        consent_model = 'td_maternal.maternalconsent'
        app_label = 'td_maternal'
