# import django_databrowse
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
# from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView

# from edc_dashboard.subject.views import additional_requisition

from .load_edc import load_edc

load_edc()

APP_NAME = settings.APP_NAME

urlpatterns = patterns(
    '',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/logout/$', RedirectView.as_view(url='/{app_name}/logout/'.format(app_name=APP_NAME))),
    (r'^admin/', include(admin.site.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),
)

# urlpatterns += patterns(
#     '',
#     url(r'^databrowse/(.*)', login_required(django_databrowse.site.root)),
# )

# urlpatterns += patterns(
#     '',
#     url(r'^databrowse/(.*)', login_required(django_databrowse.site.root)),
# )

# urlpatterns += patterns(
#     '',
#     url(r'^{app_name}/dashboard/'.format(app_name=APP_NAME),
#         include('tshilo_dikotla.apps.{app_name}_dashboard.urls'.format(app_name=APP_NAME))),
# )

urlpatterns += patterns(
    '',
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
)

urlpatterns += patterns(
    '',
    url(r'^{app_name}/$'.format(app_name=APP_NAME),
        RedirectView.as_view(url='/{app_name}/section/'.format(app_name=APP_NAME))),
    url(r'', RedirectView.as_view(url='/{app_name}/section/'.format(app_name=APP_NAME))),
)

urlpatterns += staticfiles_urlpatterns()
