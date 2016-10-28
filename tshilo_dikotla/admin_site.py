from django.contrib.admin import AdminSite

from django.apps import apps as django_apps

app_config = django_apps.get_app_config('edc_base')


class TshiloDikotlaAdminSite(AdminSite):
    site_header = app_config.project_name
    site_title = app_config.project_name
    index_title = app_config.project_name
    site_url = '/'
tshilo_dikotla_admin = TshiloDikotlaAdminSite(name='tshilo_dikotla_admin')
