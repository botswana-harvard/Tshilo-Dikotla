from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'td_maternal'
    verbose_name = 'Mothers'

    def ready(self):
        from .models.signals import (
            eligible_put_back_on_study,
            ineligible_take_off_study,
            maternal_eligibility_on_post_save)
