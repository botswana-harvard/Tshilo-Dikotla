
from django.conf.urls import url
from td_dashboard.views.subject_dashboard_view import SubjectDashboardView

urlpatterns = [
    url(r'^subject_dashboard/(?P<subject_identifier>[0-9A-Z-]+)/', SubjectDashboardView.as_view(), name='subject_dashboard_url'),
    url(r'^subject_dashboard/(?P<appointment_pk>[0-9a-z-]+)/(?P<subject_identifier>[0-9A-Z-]+)/', SubjectDashboardView.as_view(), name='subject_dashboard_url'),
]
