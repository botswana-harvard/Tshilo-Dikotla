from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'td_dashboard'
    verbose_name = 'td_dashboard'
