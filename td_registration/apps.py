from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'td_registration'
    verbose_name = 'Registration'
