from django.test.testcases import TestCase

from model_mommy import mommy

from edc_call_manager.models import Call

from .mixins import NegMotherMixin, AntenatalVisitsMotherMixin


class TestPotentialCalls(AntenatalVisitsMotherMixin, NegMotherMixin, TestCase):

    def setUp(self):
        super(TestPotentialCalls, self).setUp()

    def test_appointment_creates_potential_call(self):
        """test that creating an appointment creates a similar potential call record"""
        self.assertEqual(Call.objects.filter(subject_identifier=self.subject_identifier).count(), 1)
        mommy.make_recipe(
            'td_maternal.maternallabdel',
            subject_identifier=self.subject_identifier,
            live_infants_to_register=1)

#  TODO: Add more tests here need more clarity on this.
