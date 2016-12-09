from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'td_maternal'
    verbose_name = 'Mothers'

    def ready(self):
        from td_maternal.models.signals import (
            delete_offstudy_on_antenatalenrollment_post_delete,
            delete_offstudy_on_eligible,
            maternal_consent_on_post_save,
            maternal_eligibility_on_post_save,
            maternal_lab_del_on_post_save,
            maternal_ultrasound_initial_on_post_save,
        )
