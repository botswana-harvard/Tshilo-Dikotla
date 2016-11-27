import pprint

from dateutil.relativedelta import relativedelta
from model_mommy import mommy
from django.test import TestCase
from django.utils import timezone

from edc_registration.models import RegisteredSubject

from td_maternal.models import MaternalOffstudy

from .models import Appointment

pp = pprint.PrettyPrinter(indent=4)


class TestTd(TestCase):

    def test_registered_subject_created_by_consent(self):
        maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent')
        try:
            RegisteredSubject.objects.get(subject_identifier=maternal_consent.subject_identifier)
        except RegisteredSubject.DoesNotExist:
            self.fail('RegisteredSubject.DoesNotExist unexpectedly raised.')

    def test_appointment_maternal(self):
        """Assert no appointments for not eligible."""
        maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent')
        antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment_ineligible',
            subject_identifier=maternal_consent.subject_identifier)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.assertEqual(Appointment.objects.all().count(), 0)
        try:
            MaternalOffstudy.objects.get(subject_identifier=maternal_consent.subject_identifier)
        except MaternalOffstudy.DoesNotExist:
            self.fail('MaternalOffstudy.DoesNotExist unexpectedly raised.')

    def test_appointment_maternal2(self):
        """Assert has appointments for eligible."""
        maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent')
        antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment',
            subject_identifier=maternal_consent.subject_identifier,
            last_period_date=timezone.now() - relativedelta(days=280))
        self.assertTrue(antenatal_enrollment.is_eligible)
        self.assertEqual(Appointment.objects.all().count(), 1)
        try:
            MaternalOffstudy.objects.get(subject_identifier=maternal_consent.subject_identifier)
            self.fail('MaternalOffstudy.DoesNotExist unexpectedly NOT raised.')
        except MaternalOffstudy.DoesNotExist:
            pass
