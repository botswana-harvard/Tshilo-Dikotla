from django.conf.urls import url

from .views import MaternalDashboardView, SearchDasboardView, InfantDashboardView

urlpatterns = [
    url(r'^maternal', SearchDasboardView.as_view(), name='search_url'),
    url(r'^(?P<page>\d+)/$', SearchDasboardView.as_view(), name='subject_dashboard_url'),
    url(r'^subject_dashboard/(?P<subject_identifier>[0-9A-Z-]+)/',
        MaternalDashboardView.as_view(), name='subject_dashboard_url'),
    url(r'^subject_dashboard/(?P<subject_identifier>[0-9A-Z-]+)/(?P<page>\d+)/',
        MaternalDashboardView.as_view(), name='subject_dashboard_url'),
    url(r'^subject_dashboard/(?P<appointment_pk>[0-9a-f-]+)/(?P<subject_identifier>[0-9A-Z-]+)/',
        MaternalDashboardView.as_view(), name='subject_dashboard_url'),
    # infant url
    url(r'^infant_dashboard/(?P<subject_identifier>[0-9\-]{17})/',
        InfantDashboardView.as_view(), name='infant_subject_dashboard_url'),
    url(r'^infant_dashboard/(?P<appointment_pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/'
        '(?P<subject_identifier>[0-9\-]{17})/',
        InfantDashboardView.as_view(), name='infant_subject_dashboard_url'),
]
