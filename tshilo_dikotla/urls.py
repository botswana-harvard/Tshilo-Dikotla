from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

from edc_base.views import LoginView, LogoutView
from edc_sync.admin import edc_sync_admin

from td.admin_site import td_admin
from td_maternal.admin_site import td_maternal_admin
from td.views import HomeView, StatisticsView

APP_NAME = settings.APP_NAME

urlpatterns = [
    url(r'^admin/', td_maternal_admin.urls),
    url(r'^admin/', td_admin.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/', edc_sync_admin.urls),
    url(r'^admin/$', RedirectView.as_view(pattern_name='home_url')),
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'logout', LogoutView.as_view(pattern_name='login_url'), name='logout_url'),
    url(r'^edc-consent/', include('edc_consent.urls')),
    url(r'^edc-sync/', include('edc_sync.urls', 'edc-sync')),
    url(r'^edc_call_manager/', include('edc_call_manager.urls', 'edc-call-manager')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/logout/$', RedirectView.as_view(url='/{app_name}/logout/'.format(app_name=APP_NAME))),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^dashboard/', include('td_dashboard.urls')),
    url(r'^statistics/', StatisticsView.as_view(), name='update-statistics'),
    url(r'^edc_label/', include('edc_label.urls', namespace='edc-label')),
    url(r'^edc/', include('edc_base.urls', 'edc-base')),
    url(r'^tz_detect/', include('tz_detect.urls')),
    url(r'', HomeView.as_view(), name='home_url'),
]
