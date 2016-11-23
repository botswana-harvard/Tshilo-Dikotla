# import django_databrowse
import sys
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from edc_base.views import LoginView, LogoutView
from .admin_site import tshilo_dikotla_admin
from edc_sync.admin import edc_sync_admin

from .load_edc import load_edc

from tshilo_dikotla.views import HomeView, StatisticsView

if 'migrate' not in sys.argv and 'makemigrations' not in sys.argv:
    load_edc()

APP_NAME = settings.APP_NAME

urlpatterns = [
    url(r'^admin/', tshilo_dikotla_admin.urls),
    url(r'^admin/', admin.site.urls),
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'logout', LogoutView.as_view(pattern_name='login_url'), name='logout_url'),
    url(r'^edc-consent/', include('edc_consent.urls')),
    url(r'^edc-sync/', include('edc_sync.urls', 'edc-sync')),
#     url(r'^call_manager/$', RedirectView.as_view(pattern_name='home_url')),
#     url(r'^call_manager/', include('edc_call_manager.urls', 'call_manager')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/logout/$', RedirectView.as_view(url='/{app_name}/logout/'.format(app_name=APP_NAME))),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^{app_name}/dashboard/'.format(app_name=APP_NAME),
        include('{app_name}_dashboard.urls'.format(app_name=APP_NAME))),
    url(r'^statistics/', StatisticsView.as_view(), name='update-statistics'),
    url(r'^admin/', edc_sync_admin.urls),
    url(r'^edc_label/', include('edc_label.urls', namespace='edc-label')),
    url(r'^edc/', include('edc_base.urls', 'edc-base')),
    url(r'^admin/$', RedirectView.as_view(pattern_name='home_url')),
    url(r'', HomeView.as_view(), name='home_url'),
]

urlpatterns += staticfiles_urlpatterns()
