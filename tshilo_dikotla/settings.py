"""
Django settings for tshilo_dikotla project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import sys
import os
import configparser
import socket
from unipath import Path

from django.utils import timezone

from .databases import (
    PRODUCTION_POSTGRES, TEST_HOSTS_POSTGRES, TRAVIS_POSTGRES, PRODUCTION_SECRET_KEY)


# EDC specific settings
APP_NAME = 'td'
LIVE_SERVER = 'td.bhp.org.bw'
TEST_HOSTS = ['edc4.bhp.org.bw', 'tdtest.bhp.org.bw']
DEVELOPER_HOSTS = [
    'mac2-2.local', 'ckgathi', 'one-2.local', 'One-2.local', 'tsetsiba', 'leslie']

PROJECT_TITLE = 'tshilo_dikotla.apps.AppConfig.verbose_name'
SOURCE_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(1)
BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
MEDIA_ROOT = BASE_DIR.child('media')
PROJECT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
PROJECT_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(1)
ETC_DIR = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(2).child('etc')

if socket.gethostname() == LIVE_SERVER:
    KEY_PATH = '/home/django/source/tshilo_dikotla/keys'
elif socket.gethostname() in TEST_HOSTS + DEVELOPER_HOSTS:
    KEY_PATH = os.path.join(SOURCE_ROOT, 'crypto_fields')
elif 'test' in sys.argv:
    KEY_PATH = os.path.join(SOURCE_ROOT, 'crypto_fields')
else:
    raise TypeError(
        'Warning! Unknown hostname for KEY_PATH. \n'
        'Getting this wrong on a LIVE SERVER will corrupt your encrypted data!!! \n'
        'Expected hostname to appear in one of '
        'settings.LIVE_SERVER, settings.TEST_HOSTS or settings.DEVELOPER_HOSTS. '
        'Got hostname=\'{}\'\n'.format(socket.gethostname()))

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']


INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_history',
    'rest_framework',
    'rest_framework.authtoken',
    'django_js_reverse',
    'corsheaders',
    'crispy_forms',
#     'edc_templates',  # for what?
#     'edc_configuration',  # ???
#     'edc_appointment.apps.AppConfig',
    'django_revision.apps.AppConfig',
    'django_crypto_fields.apps.AppConfig',
    'edc_call_manager.apps.AppConfig',
    'django_appconfig_ini',
    'edc_content_type_map.apps.AppConfig',
#     'edc_dashboard.apps.AppConfig',
    # 'edc_data_manager.apps.AppConfig', # not ready
    'edc_lab',
    'edc_code_lists',
    'edc_death_report.apps.AppConfig',
    'edc_device.apps.AppConfig',
    'edc_locator.apps.AppConfig',
    'edc_offstudy.apps.AppConfig',
    'edc_rule_groups.apps.AppConfig',
    'edc_sync_files.apps.AppConfig',
    'td_call_manager.apps.AppConfig',
#     'td_dashboard.apps.AppConfig',
    'td_infant.apps.AppConfig',
    'td_lab.apps.AppConfig',
    'td_list.apps.AppConfig',
    'td_maternal.apps.AppConfig',
    'td_appointment.apps.AppConfig',
    'td_registration.apps.AppConfig',
    'edc_visit_schedule.apps.AppConfig',
    'tshilo_dikotla.apps.EdcVisitTrackingAppConfig',
    'tshilo_dikotla.apps.EdcProtocolAppConfig',
    'tshilo_dikotla.apps.EdcBaseAppConfig',
    'tshilo_dikotla.apps.EdcConsentAppConfig',
    'tshilo_dikotla.apps.EdcLabelAppConfig',
    'tshilo_dikotla.apps.EdcRegistrationAppConfig',
    'tshilo_dikotla.apps.EdcAppointmentAppConfig',
    'tshilo_dikotla.apps.EdcSyncAppConfig',
    'tshilo_dikotla.apps.AppConfig',
    'tshilo_dikotla.apps.EdcIdentifierAppConfig',
    'tshilo_dikotla.apps.EdcMetadataAppConfig',
    'tshilo_dikotla.apps.EdcTimepointAppConfig'
]

if 'test' in sys.argv:
    # TODO: Make this list auto generate from INSTALLED_APPS
    # Ignore running migrations on unit tests, greately speeds up tests.
    MIGRATION_MODULES = {"td_lab": None,
                         "td_infant": None,
                         "td_maternal": None,
                         "edc_registration": None,
                         "edc_content_type_map": None,
                         "edc_appointment": None,
                         "call_manager": None,
                         "edc_death_report": None,
                         "edc_identifier": None,
                         "edc_meta_data": None,
                         "edc_consent": None,
                         "edc_rule_groups": None,
                         "edc_data_manager": None,
                         #"lab_packing": None,
                         "lab_clinic_api": None,
                         'django_crypto_fields': None,
                         "lab_clinic_reference": None,
                         "edc_death_report": None,
                         "edc_sync": None,
                         "edc_code_lists": None,
                         "edc_configuration": None,
                         "td_list": None,
                         "call_manager": None,
                         "edc_visit_schedule": None,
                         "edc_visit_tracking": None,
                         "edc_offstudy": None}

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages")

ROOT_URLCONF = 'tshilo_dikotla.urls'

TEMPLATE_DIRS = ()

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader')

WSGI_APPLICATION = 'tshilo_dikotla.wsgi.application'

SECRET_KEY = 'sdfsd32fs#*@(@dfsdf'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


if socket.gethostname() in DEVELOPER_HOSTS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    }
elif socket.gethostname() == LIVE_SERVER:
    SECRET_KEY = PRODUCTION_SECRET_KEY
    DATABASES = PRODUCTION_POSTGRES
elif socket.gethostname() in TEST_HOSTS:
    DATABASES = TEST_HOSTS_POSTGRES
elif 'test' in sys.argv:
    DATABASES = TRAVIS_POSTGRES

FIELD_MAX_LENGTH = 'default'

# Internationalization
LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('tn', 'Setswana'),
    ('en', 'English'))

TIME_ZONE = 'Africa/Gaborone'

USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.child('static')

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# edc.crytpo_fields encryption keys
# developers should set by catching their hostname instead of setting explicitly

GIT_DIR = BASE_DIR.ancestor(1)

STUDY_OPEN_DATETIME = timezone.datetime(2015, 10, 18, 0, 0, 0)

SUBJECT_APP_LIST = ['maternal', 'infant']
SUBJECT_TYPES = ['maternal', 'infant']
MAX_SUBJECTS = {'maternal': 3000, 'infant': 3000}
MINIMUM_AGE_OF_CONSENT = 18
MAXIMUM_AGE_OF_CONSENT = 64
AGE_IS_ADULT = 18
GENDER_OF_CONSENT = ['F']
DISPATCH_APP_LABELS = []

if socket.gethostname() == LIVE_SERVER:
    DEVICE_ID = 99
    PROJECT_TITLE = '{} Live Server'.format(PROJECT_TITLE)
elif socket.gethostname() in TEST_HOSTS:
    DEVICE_ID = 99
    PROJECT_TITLE = 'TEST (postgres): {}'.format(PROJECT_TITLE)
elif socket.gethostname() in DEVELOPER_HOSTS:
    DEVICE_ID = 99
    PROJECT_TITLE = 'TEST (sqlite3): {}'.format(PROJECT_TITLE)
elif 'test' in sys.argv:
    DEVICE_ID = 99
    PROJECT_TITLE = 'TEST (sqlite3): {}'.format(PROJECT_TITLE)
else:
    raise ImproperlyConfigured(
        'Unknown hostname for full PROJECT_TITLE. Expected hostname to appear in one of '
        'settings.LIVE_SERVER, settings.TEST_HOSTS or settings.DEVELOPER_HOSTS. '
        'Got hostname=\'{}\''.format(socket.gethostname()))

SITE_CODE = '40'
CELLPHONE_REGEX = '^[7]{1}[12345678]{1}[0-9]{6}$'
TELEPHONE_REGEX = '^[2-8]{1}[0-9]{6}$'
DEFAULT_STUDY_SITE = '40'
ALLOW_MODEL_SERIALIZATION = True

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'
MEDIA_ROOT = BASE_DIR.child('media')

try:
    config = configparser.ConfigParser()
    config.read(os.path.join(ETC_DIR, 'edc_sync.ini'))
    CORS_ORIGIN_WHITELIST = tuple(config['corsheaders'].get('cors_origin_whitelist').split(','))
    CORS_ORIGIN_ALLOW_ALL = config['corsheaders'].getboolean('cors_origin_allow_all', True)
except KeyError:
    CORS_ORIGIN_WHITELIST = None
    CORS_ORIGIN_ALLOW_ALL = True
REST_FRAMEWORK = {
    'PAGE_SIZE': 1,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# EDC_SYNC_ROLE = 'client'
