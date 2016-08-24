from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'td_list'
    verbose_name = 'Lists'
