from django.contrib.admin import AdminSite

from django.apps import apps as django_apps

app_config = django_apps.get_app_config('edc_base')


class TdMaternalAdminSite(AdminSite):
    site_title = '{} {}'.format(app_config.project_name, 'Maternal')
    site_header = '{} {}'.format(app_config.project_name, 'Maternal')
    index_title = '{} {}'.format(app_config.project_name, 'Maternal')
    site_url = '/'
td_maternal_admin = TdMaternalAdminSite(name='td_maternal_admin')


class TdMaternalHistoricalAdminSite(AdminSite):
    site_title = app_config.project_name + ' (Historical)'
    site_header = app_config.project_name + ' (Historical)'
    index_title = app_config.project_name + ' (Historical)'
    site_url = '/'
td_maternal_historical_admin = TdMaternalHistoricalAdminSite(name='td_maternal_historical_admin')
