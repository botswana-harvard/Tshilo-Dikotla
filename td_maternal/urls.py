from django.conf.urls import url

from td_maternal.admin_site import td_maternal_admin

urlpatterns = [
    url(r'^admin/', td_maternal_admin.urls),
]
