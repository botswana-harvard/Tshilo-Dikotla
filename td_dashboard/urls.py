from django.conf.urls import url

from .views import MaternalDashboardView, SearchDashboardView  #, InfantDashboardView

urlpatterns = [
    url(r'^subject/(?P<subject_identifier>[0-9A-Z-]+)/(?P<selected_appointment>[0-9a-f-]+)/',
        MaternalDashboardView.as_view(), name='maternal_dashboard_url'),
    url(r'^subject/(?P<subject_identifier>[0-9A-Z-]+)/(?P<page>\d+)/',
        MaternalDashboardView.as_view(), name='maternal_dashboard_url'),
    url(r'^subject/(?P<subject_identifier>[0-9A-Z-]+)/',
        MaternalDashboardView.as_view(), name='maternal_dashboard_url'),
    url(r'^search/(?P<page>\d+)/$', SearchDashboardView.as_view(), name='search_url'),
    url(r'^search/$', SearchDashboardView.as_view(), name='search_url'),
    # infant url
#     url(r'^infant_dashboard/(?P<subject_identifier>[0-9\-]{17})/',
#         InfantDashboardView.as_view(), name='subject_dashboard_url'),
#     url(r'^infant_dashboard/(?P<appointment>[0-9a-f-]+)/(?P<subject_identifier>[0-9\-]{17})/',
#         InfantDashboardView.as_view(), name='infant_subject_dashboard_url'),
]
