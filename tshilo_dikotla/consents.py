import pytz

from dateutil.tz import gettz
from datetime import datetime

from django.apps import apps as django_apps

from edc_consent.consent import Consent
from edc_consent.site_consents import site_consents
from edc_constants.constants import FEMALE

app_config = django_apps.get_app_config('edc_protocol')

tzinfo = gettz('Africa/Gaborone')

consent = Consent(
            'td_maternal.maternalconsent',
            start=datetime(2016, 5, 1, 0, 0, 0, tzinfo=pytz.utc),
            end=datetime(2022, 12, 1, 0, 0, 0, tzinfo=pytz.utc),
            version='1',
            age_min=18,
            age_is_adult=18,
            age_max=50,
            gender=[FEMALE])

site_consents.register(consent)
