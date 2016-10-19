
from django.conf.urls import url
from td_dashboard.views.maternal_dashboard_view import MaternalDashboardView
from td_dashboard.views.search_dashboard_view import SearchDasboardView

urlpatterns = [
    url(r'^maternal', SearchDasboardView.as_view(), name='search_url'),
    url(r'^subject_dashboard/(?P<subject_identifier>[0-9A-Z-]+)/', MaternalDashboardView.as_view(), name='subject_dashboard_url'),
    url(r'^subject_dashboard/(?P<appointment_pk>[0-9a-f-]+)/(?P<subject_identifier>[0-9A-Z-]+)/', MaternalDashboardView.as_view(), name='subject_dashboard_url'),
]
