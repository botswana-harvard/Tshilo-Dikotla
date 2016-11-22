from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'td_maternal'
    verbose_name = 'Mothers'

    def ready(self):
        from .signals import *
