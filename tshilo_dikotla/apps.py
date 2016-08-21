import os

from django.utils import timezone

from django.apps import AppConfig
from django.conf import settings

from django_crypto_fields.apps import AppConfig as DjangoCryptoFieldsAppConfigParent
from edc_consent.apps import EdcConsentAppConfig
from edc_label.apps import AppConfig as EdcLabelConfigParent
from edc_sync.apps import AppConfig as EdcSyncAppConfigParent
from edc_sync.constants import SERVER

study_start_datetime = timezone.datetime(2016, 4, 1, 0, 0, 0)
study_end_datetime = timezone.datetime(2016, 12, 1, 0, 0, 0)

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
         'version': '1'}
    ]


class DjangoCryptoFieldsAppConfig(DjangoCryptoFieldsAppConfigParent):
    name = 'django_crypto_fields'
    model = ('django_crypto_fields', 'crypt')


class EdcSyncAppConfig(EdcSyncAppConfigParent):
    name = 'edc_sync'
    role = edc_sync_role


class EdcLabelAppConfig(EdcLabelConfigParent):
    default_cups_server_ip = '10.113.201.203'
    default_printer_label = 'tshilo_testing'
    default_template_file = os.path.join(settings.STATIC_ROOT, 'tshilo_dikotla', 'label_templates', 'aliquot.lbl')
    default_label_identifier_name = ''
