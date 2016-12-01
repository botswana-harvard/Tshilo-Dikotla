from td.admin_mixins import ModelAdminMixin
from ..models import MaternalVisit
# from django.urls.base import reverse
from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin


class BaseMaternalModelAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin):

    dashboard_type = 'maternal'
    visit_model_name = 'maternalvisit'

    def redirect_url(self, request, obj, post_url_continue=None):
        return request.GET.get('next')

#     def redirect_url(self, request, obj, post_url_continue=None):
#         args = request.GET.dict()
#         args.pop('visit_code')
#         url_name = request.GET.get(self.querystring_name)
#         subject_identifier = request.GET.get('subject_identifier')
#         appointment_id = request.GET.get('appointment_pk')
#         dashboard_url = reverse(url_name, kwargs={'appointment_pk': appointment_id, 'subject_identifier': subject_identifier})
#         show = 'show={}'.format(request.GET.get('show', None))
#         next_url = "{}?{}".format(dashboard_url, show)
#         return next_url

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
            if request.GET.get('subject_identifier'):
                kwargs["queryset"] = MaternalVisit.objects.filter(
                    appointment__subject_identifier=request.GET.get('subject_identifier'),
                    appointment__visit_code=request.GET.get('visit_code'))
        return super(BaseMaternalModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
