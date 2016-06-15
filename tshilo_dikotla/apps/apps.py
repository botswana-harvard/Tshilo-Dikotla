# from datetime import datetime
from django.utils import timezone

from django.apps import AppConfig

from edc_consent.apps import EdcConsentAppConfig

study_start_datetime = timezone.datetime(2016, 4, 1, 0, 0, 0)
study_end_datetime = timezone.datetime(2016, 12, 1, 0, 0, 0)


class TshiloDikotlaConfig(AppConfig):
    name = 'tshilo_dikotla'
    verbose_name = 'Tshilo Dikotla'


class ConsentAppConfig(EdcConsentAppConfig):

    consent_type_setup = [
        {'app_label': 'td_maternal',
         'model_name': 'maternalconsent',
         'start_datetime': study_start_datetime,
         'end_datetime': study_end_datetime,
         'version': '1'}
    ]

