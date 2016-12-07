from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'td_maternal'
    verbose_name = 'Mothers'

    def ready(self):
        from .models.signals import (
            delete_offstudy_on_eligible,
            create_offstudy_on_ineligible,
            maternal_eligibility_on_post_save)
