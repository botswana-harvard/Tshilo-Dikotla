from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'td_lab'
    verbose_name = 'Labs'
