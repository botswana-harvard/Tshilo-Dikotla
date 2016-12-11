from django.test.testcases import TestCase

from td.models import Appointment

from td_maternal.tests.test_mixins import CompleteMaternalCrfsMixin, PosMotherMixin, DeliverMotherMixin
from model_mommy import mommy


class TestInfantBirth(DeliverMotherMixin, CompleteMaternalCrfsMixin, PosMotherMixin, TestCase):

    def setUp(self):
        self.maternal_identifier = self.create_mother()

    def test_birth(self):
        infant_birth = mommy.make_recipe(
            'td_infant.infantbirth',
            delivery_reference=self.maternal_labour_del,
            registered_subject=self.infant_registered_subject)
        self.assertEqual(Appointment.objects.filter(
            subject_identifier=infant_birth.registered_subject.subject_identifier).count(), 9)
