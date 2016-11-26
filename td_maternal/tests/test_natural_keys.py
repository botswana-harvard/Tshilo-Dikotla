from django.apps import apps as django_apps

from .base_test_case import BaseTestCase


class TestNaturalKey(BaseTestCase):

    def test_natural_key_maternal(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        td_maternal_models = django_apps.get_app_config('td_maternal').get_models()
        for model in td_maternal_models:
            if 'Audit' not in model._meta.object_name:
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_natural_key_infant(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        td_maternal_models = django_apps.get_app_config('td_infant').get_models()
        for model in td_maternal_models:
            if 'Audit' not in model._meta.object_name:
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_natural_key_lab(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        td_maternal_models = django_apps.get_app_config('td_lab').get_models()
        for model in td_maternal_models:
            if 'Audit' not in model._meta.object_name:
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_natural_key_appointment(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        td_maternal_models = django_apps.get_app_config('td').get_models()
        for model in td_maternal_models:
            if 'Audit' not in model._meta.object_name:
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))
