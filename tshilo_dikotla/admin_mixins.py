from django.core.urlresolvers import reverse

from edc_base.modeladmin.mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
    ModelAdminAuditFieldsMixin)


class EdcBaseModelAdminMixin(ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
                             ModelAdminAuditFieldsMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


class SectionRedirectUrlMixin(ModelAdminNextUrlRedirectMixin):

    def redirect_url(self, request, obj, post_url_continue=None):
        url_name = request.GET.get(self.querystring_name)
        section_name = request.GET.get('section_name')
        return reverse(url_name, kwargs={'section_name': section_name})


class DashboardRedirectUrlMixin(ModelAdminNextUrlRedirectMixin):

    def redirect_url(self, request, obj, post_url_continue=None):
        url_name = request.GET.get(self.querystring_name)
        dashboard_type = request.GET.get('dashboard_type')
        dashboard_model = request.GET.get('dashboard_model')
        dashboard_id = request.GET.get('dashboard_id')
        show = request.GET.get('show')
        return reverse(url_name, kwargs={
            'dashboard_type': dashboard_type,
            'dashboard_model': dashboard_model,
            'dashboard_id': dashboard_id,
            'show': show})
