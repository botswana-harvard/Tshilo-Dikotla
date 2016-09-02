# import django_databrowse
import sys
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView

from edc_dashboard.subject.views import additional_requisition
from edc_sync.admin import edc_sync_admin

from .load_edc import load_edc

from tshilo_dikotla.views import HomeView, StatisticsView

if 'migrate' not in sys.argv and 'makemigrations' not in sys.argv:
    load_edc()

APP_NAME = settings.APP_NAME

# urlpatterns = patterns(
#     '',
#     (r'^admin/doc/', include('django.contrib.admindocs.urls')),
#     (r'^admin/logout/$', RedirectView.as_view(url='/{app_name}/logout/'.format(app_name=APP_NAME))),
#     (r'^admin/', include(admin.site.urls)),
#     (r'^i18n/', include('django.conf.urls.i18n')),
# )
# 
# 
# urlpatterns += patterns(
#     '',
#     url(r'^{app_name}/dashboard/'.format(app_name=APP_NAME),
#         include('{app_name}_dashboard.urls'.format(app_name=APP_NAME))),
# )
# 
# # urlpatterns += patterns(
# #     '',
# #     url(r'^databrowse/(.*)', login_required(django_databrowse.site.root)),
# # )
# 
# urlpatterns += patterns(
#     '',
#     url(r'^{app_name}/dashboard/visit/add_requisition/'.format(app_name=APP_NAME),
#         additional_requisition, name="add_requisition"),
# )
# 
# 
# urlpatterns += patterns(
#     '',
#     url(r'^{app_name}/login/'.format(app_name=APP_NAME),
#         'django.contrib.auth.views.login',
#         name='{app_name}_login'.format(app_name=APP_NAME)),
#     url(r'^{app_name}/logout/'.format(app_name=APP_NAME),
#         'django.contrib.auth.views.logout_then_login',
#         name='{app_name}_logout'.format(app_name=APP_NAME)),
#     url(r'^{app_name}/password_change/'.format(app_name=APP_NAME),
#         'django.contrib.auth.views.password_change',
#         name='password_change_url'.format(app_name=APP_NAME)),
#     url(r'^{app_name}/password_change_done/'.format(app_name=APP_NAME),
#         'django.contrib.auth.views.password_change_done',
#         name='password_change_done'.format(app_name=APP_NAME)),
# )
# 
# urlpatterns += patterns(
#     '',
#     url(r'^{app_name}/section/'.format(app_name=APP_NAME), include('edc_dashboard.section.urls'), name='section'),
# )
# 
# urlpatterns += patterns(
#     '',
#     url(r'^{app_name}/$'.format(app_name=APP_NAME),
#         RedirectView.as_view(url='/{app_name}/section/'.format(app_name=APP_NAME))),
#     url(r'', RedirectView.as_view(url='/{app_name}/section/'.format(app_name=APP_NAME))),
# )

urlpatterns = [
    #'',
    url(r'', include('edc_base.urls')),
    url(r'^edc-consent/', include('edc_consent.urls')),
    url(r'^edc-sync/', include('edc_sync.urls', 'edc-sync')),
    url(r'^edc-sync-files/', include('edc_sync_files.urls', 'edc-sync-files')),
    url(r'^call_manager/$', RedirectView.as_view(pattern_name='home_url')),
    url(r'^call_manager/', include('edc_call_manager.urls', 'call_manager')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/logout/$', RedirectView.as_view(url='/{app_name}/logout/'.format(app_name=APP_NAME))),
#     url(r'^admin/', call_manager_admin.urls),
    url(r'^admin/', edc_sync_admin.urls),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^{app_name}/dashboard/'.format(app_name=APP_NAME),
        include('{app_name}_dashboard.urls'.format(app_name=APP_NAME))),
    url(r'^{app_name}/dashboard/visit/add_requisition/'.format(app_name=APP_NAME),
        additional_requisition, name="add_requisition"),
    url(r'^{app_name}/login/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.login',
        name='{app_name}_login'.format(app_name=APP_NAME)),
    url(r'^{app_name}/logout/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.logout_then_login',
        name='{app_name}_logout'.format(app_name=APP_NAME)),
    url(r'^{app_name}/password_change/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.password_change',
        name='password_change_url'.format(app_name=APP_NAME)),
    url(r'^{app_name}/password_change_done/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.password_change_done',
        name='password_change_done'.format(app_name=APP_NAME)),
    url(r'^{app_name}/section/'.format(app_name=APP_NAME), include('edc_dashboard.section.urls'), name='section'),
    url(r'^{app_name}/$'.format(app_name=APP_NAME),
        RedirectView.as_view(url='/{app_name}/section/'.format(app_name=APP_NAME))),
    url(r'^statistics/', StatisticsView.as_view(), name='update-statistics'),
    url(r'^home/', HomeView.as_view(), name='home_url'),
    url(r'^', HomeView.as_view(), name='home_url'),
    url(r'', RedirectView.as_view(url='/{app_name}/section/'.format(app_name=APP_NAME))),
]

urlpatterns += staticfiles_urlpatterns()
