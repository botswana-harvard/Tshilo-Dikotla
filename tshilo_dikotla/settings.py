import os
import socket
import sys

from unipath import Path

from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured

from tshilo_dikotla.config.databases import (
    PRODUCTION_MYSQL, TEST_HOSTS_MYSQL, TRAVIS_MYSQL, PRODUCTION_SECRET_KEY)

# these help select the KEY_PATH and full project title
LIVE_SERVER = 'tshilo_dikotla.bhp.org.bw'

TEST_HOSTS = ['edc4.bhp.org.bw']
DEVELOPER_HOSTS = [
    'mac2-2.local', 'ckgathi', 'one-2.local', 'One-2.local', 'tsetsiba', 'leslie']

APP_NAME = 'td'
PROJECT_TITLE = 'Tshilo Dikotla'
INSTITUTION = 'Botswana-Harvard AIDS Institute'
PROTOCOL_REVISION = 'v1.0'
PROTOCOL_NUMBER = '085'

SOURCE_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(1)
BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
MEDIA_ROOT = BASE_DIR.child('media')
PROJECT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
PROJECT_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(1)

if socket.gethostname() == LIVE_SERVER:
    KEY_PATH = '/home/django/source/tshilo_dikotla/keys'
elif socket.gethostname() in TEST_HOSTS + DEVELOPER_HOSTS:
    KEY_PATH = os.path.join(SOURCE_ROOT, 'crypto_fields/test_keys')
elif 'test' in sys.argv:
    KEY_PATH = os.path.join(SOURCE_ROOT, 'crypto_fields/test_keys')
else:
    raise TypeError(
        'Warning! Unknown hostname for KEY_PATH. \n'
        'Getting this wrong on a LIVE SERVER will corrupt your encrypted data!!! \n'
        'Expected hostname to appear in one of '
        'settings.LIVE_SERVER, settings.TEST_HOSTS or settings.DEVELOPER_HOSTS. '
        'Got hostname=\'{}\'\n'.format(socket.gethostname()))

DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'edc_templates',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_history',
    'django_revision',
    'django_crypto_fields',
    'south',
    'edc_appointment',
    'edc_base',
    'edc_call_manager',
    'edc_consent',
    'edc_constants',
    'edc_content_type_map',
    'edc_dashboard',
    'edc_data_manager',
    'edc_death_report',
    'edc_device',
    'edc_identifier',
    'edc_lab',
    'edc_meta_data',
    'edc_offstudy',
    'edc_registration',
    'edc_rule_groups',
    'edc_sync',
    'edc_visit_schedule',
    'edc_visit_tracking',
    'tshilo_dikotla.apps.td_maternal',
]

if 'test' in sys.argv:
    INSTALLED_APPS.append('edc_testing')

if socket.gethostname() in DEVELOPER_HOSTS + TEST_HOSTS or 'test' in sys.argv:
    INSTALLED_APPS.pop(INSTALLED_APPS.index('south'))
INSTALLED_APPS = tuple(INSTALLED_APPS)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',)

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
# Database
if socket.gethostname() in DEVELOPER_HOSTS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
        'test_server': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    }
elif socket.gethostname() == LIVE_SERVER:
    SECRET_KEY = PRODUCTION_SECRET_KEY
    DATABASES = PRODUCTION_MYSQL
elif socket.gethostname() in TEST_HOSTS:
    DATABASES = TEST_HOSTS_MYSQL
elif 'test' in sys.argv:
    DATABASES = TRAVIS_MYSQL

# django auth
AUTH_PROFILE_MODULE = "bhp_userprofile.userprofile"

PROJECT_NUMBER = 'BHP085'
PROJECT_IDENTIFIER_PREFIX = '085'
PROJECT_IDENTIFIER_MODULUS = 7
IS_SECURE_DEVICE = True
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

# admin
LOGIN_URL = '/{app_name}/login/'.format(app_name=APP_NAME)
LOGIN_REDIRECT_URL = '/{app_name}/'.format(app_name=APP_NAME)
LOGOUT_URL = '/{app_name}/logout/'.format(app_name=APP_NAME)

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
    PROJECT_TITLE = 'TEST (mysql): {}'.format(PROJECT_TITLE)
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
SERVER_DEVICE_ID_LIST = [91, 92, 93, 94, 95, 96, 97, 99]
MIDDLEMAN_DEVICE_ID_LIST = [98]
if str(DEVICE_ID) == '98':
    PROJECT_TITLE = 'RESERVED FOR MIDDLE MAN'

CELLPHONE_REGEX = '^[7]{1}[12345678]{1}[0-9]{6}$'
TELEPHONE_REGEX = '^[2-8]{1}[0-9]{6}$'
DEFAULT_STUDY_SITE = '40'
ALLOW_MODEL_SERIALIZATION = True
