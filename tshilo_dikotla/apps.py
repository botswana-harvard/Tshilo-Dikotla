# from datetime import datetime
from django.utils import timezone

from django.apps import AppConfig
from django.conf import settings

from django_crypto_fields.apps import AppConfig as DjangoCryptoFieldsAppConfigParent
from edc_consent.apps import EdcConsentAppConfig
from edc_sync.apps import AppConfig as EdcSyncAppConfigParent
from edc_sync.constants import SERVER

study_start_datetime = timezone.datetime(2016, 4, 1, 0, 0, 0)
consent_study_version_1_end = timezone.datetime(2017, 4, 18, 0, 0, 0)
consent_version_2_start = timezone.datetime(2018, 1, 31, 0, 0, 0)
study_end_datetime = timezone.datetime(2018, 12, 1, 0, 0, 0)

try:
    edc_sync_role = settings.EDC_SYNC_ROLE
except AttributeError:
    edc_sync_role = SERVER


class TshiloDikotlaConfig(AppConfig):
    name = 'tshilo_dikotla'
    institution = 'Botswana Harvard AIDS Institute Partnership'
    verbose_name = 'Tshilo Dikotla'


class ConsentAppConfig(EdcConsentAppConfig):

    consent_type_setup = [
        {'app_label': 'td_maternal',
         'model_name': 'maternalconsent',
         'start_datetime': study_start_datetime,
         'end_datetime': study_end_datetime,
         'version': '1'},
        {'app_label': 'td_maternal',
         'model_name': 'maternalconsent',
         'start_datetime': consent_version_2_start,
         'end_datetime': study_end_datetime,
         'version': '3'},
    ]


class DjangoCryptoFieldsAppConfig(DjangoCryptoFieldsAppConfigParent):
    name = 'django_crypto_fields'
    model = ('django_crypto_fields', 'crypt')


class EdcSyncAppConfig(EdcSyncAppConfigParent):
    name = 'edc_sync'
    role = edc_sync_role
