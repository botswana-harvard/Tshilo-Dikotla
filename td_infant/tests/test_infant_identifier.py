from model_mommy import mommy

from django.apps import apps as django_apps
from django.test import TestCase

from td_maternal.tests.test_mixins import MotherMixin


class TestInfantIdentifier(MotherMixin, TestCase):

    def setUp(self):
        super(TestInfantIdentifier, self).setUp()
        self.subject_identifier = None
        self.maternal_identifier = self.maternal_consent.subject_identifier

    def test_infant_identifier(self):
        RegisteredSubject = django_apps.get_app_config('edc_registration').model
        mommy.make_recipe(
            'td_maternal.maternallabdel',
            subject_identifier=self.maternal_identifier,
            live_infants_to_register=1,
            live_infants=1)
        try:
            RegisteredSubject.objects.get(relative_identifier=self.maternal_identifier)
        except RegisteredSubject.DoesNotExist:
            self.fail('RegisteredSubject.DoesNotExist raised unexpectedly')

    def test_infant_identifier2(self):
        RegisteredSubject = django_apps.get_app_config('edc_registration').model
        mommy.make_recipe(
            'td_maternal.maternallabdel',
            subject_identifier=self.maternal_identifier,
            live_infants_to_register=1,
            live_infants=3,
            birth_orders='1')
        try:
            RegisteredSubject.objects.get(relative_identifier=self.maternal_identifier)
        except RegisteredSubject.DoesNotExist:
            self.fail('RegisteredSubject.DoesNotExist raised unexpectedly')

    def test_infant_birth_updates_registered_subject(self):
        RegisteredSubject = django_apps.get_app_config('edc_registration').model
        maternal_lab_del = mommy.make_recipe(
            'td_maternal.maternallabdel',
            subject_identifier=self.maternal_identifier,
            live_infants_to_register=1,
            live_infants=3,
            birth_orders='2')
        obj = RegisteredSubject.objects.get(relative_identifier=self.maternal_identifier)
        self.assertTrue(obj.first_name.startswith('Baby2'))
        mommy.make_recipe(
            'td_infant.infantbirth',
            delivery_reference=maternal_lab_del.reference,
            first_name='Holden',
            birth_order=2)
        obj = RegisteredSubject.objects.get(relative_identifier=self.maternal_identifier)
        self.assertEqual(obj.first_name, 'Holden')
