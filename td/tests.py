from model_mommy import mommy

from django.test import TestCase

from .models import Appointment
from edc_registration.models import RegisteredSubject


class TestTd(TestCase):

    def test_registered_subject_created_by_consent(self):
        maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent')
        try:
            RegisteredSubject.objects.get(subject_identifier=maternal_consent.subject_identifier)
        except RegisteredSubject.DoesNotExist:
            self.fail('RegisteredSubject.DoesNotExist unexpectedly raise ')

    def test_appointment_maternal(self):
        maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent')
        try:
            RegisteredSubject.objects.get(subject_identifier=maternal_consent.subject_identifier)
        except RegisteredSubject.DoesNotExist:
            self.fail('RegisteredSubject.DoesNotExist unexpectedly raise ')
        mommy.make_recipe(
            'td_maternal.antenatalenrollment_ineligible',
            subject_identifier=maternal_consent.subject_identifier)
        self.assertEqual(Appointment.objects.all().count(), 0)

    def test_appointment_maternal2(self):
        maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent')
        try:
            RegisteredSubject.objects.get(subject_identifier=maternal_consent.subject_identifier)
        except RegisteredSubject.DoesNotExist:
            self.fail('RegisteredSubject.DoesNotExist unexpectedly raise ')
        mommy.make_recipe(
            'td_maternal.antenatalenrollment',
            subject_identifier=maternal_consent.subject_identifier)
        self.assertEqual(Appointment.objects.all().count(), 1)
