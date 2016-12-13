from django.test.testcases import TestCase

from td.models import Appointment

from .test_mixins import InfantMixin
from model_mommy import mommy


class TestInfantBirth(InfantMixin, TestCase):

    def setUp(self):
        super(TestInfantBirth, self).setUp()

    def test_birth(self):
        self.make_infant_birth()
        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.infant_identifier).count(), 9)
