from django.test import TestCase

from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NO
from edc_visit_tracking.constants import SCHEDULED

from td.models import Appointment

from ..forms import InfantFuForm
from .test_mixins import InfantMixin


class TestInfantFu(InfantMixin, TestCase):

    def setUp(self):
        super(TestInfantFu, self).setUp()
        self.make_infant_birth(maternal_status=POS)
        infant_appointment_2000 = Appointment.objects.get(subject_identifier=self.infant_identifier, visit_code='2000')
        mommy.make_recipe(
            'td_infant.infantvisit',
            appointment=infant_appointment_2000,
            report_datetime=infant_appointment_2000.appt_datetime,
            reason=SCHEDULED)

        self.options = {
            'report_datetime': get_utcnow(),
            'infant_birth': self.infant_birth.id,
            'infant_visit': self.get_infant_visit('2000').id,
            'physical_assessment': NO,
            'diarrhea_illness': NO,
            'has_dx': NO,
            'was_hospitalized': NO,
        }

    def test_infant_hospitalization(self):
        self.options.update(
            infant_birth=self.get_infant_visit('2000').id,
            was_hospitalized=YES)
        infant_fu = InfantFuForm(data=self.options)
        self.assertIn(
            'If infant was hospitalized, please provide # of days hospitalized',
            infant_fu.errors.get('__all__'))

    def test_validate_hospitalization_duration(self):
        self.options.update(
            infant_birth=self.get_infant_visit('2000').id,
            was_hospitalized=YES,
            days_hospitalized=100)
        infant_fu = InfantFuForm(data=self.options)
        self.assertIn(
            'days hospitalized cannot be greater than 90days',
            infant_fu.errors.get('__all__'))
