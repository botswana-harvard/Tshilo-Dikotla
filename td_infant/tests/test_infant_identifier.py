from django.apps import apps as django_apps
from td_infant.tests.mixins import MaternalMixin
from django.test import TestCase
from model_mommy import mommy


class TestInfantIdentifier(TestCase, MaternalMixin):

    def setUp(self):
        self.maternal_identifier = self.create_mother()

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
