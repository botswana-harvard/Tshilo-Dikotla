from django.contrib.admin import AdminSite

from django.apps import apps as django_apps

app_config = django_apps.get_app_config('edc_base')


class TdInfantAdminSite(AdminSite):
    site_title = app_config.project_name
    site_header = app_config.project_name
    index_title = app_config.project_name
    site_url = '/'
td_infant_admin = TdInfantAdminSite(name='td_infant_admin')


class TdInfantHistoricalAdminSite(AdminSite):
    site_title = app_config.project_name + ' (Historical)'
    site_header = app_config.project_name + ' (Historical)'
    index_title = app_config.project_name + ' (Historical)'
    site_url = '/'
td_infant_historical_admin = TdInfantHistoricalAdminSite(name='td_infant_historical_admin')
