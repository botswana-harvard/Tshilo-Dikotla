from copy import copy

from django.contrib import admin

from edc_lab.modeladmin_mixins import RequisitionAdminMixin

from td_maternal.models import MaternalVisit

from ..forms import MaternalRequisitionForm
from ..models import MaternalRequisition, Panel
# from tshilo_dikotla.admin_mixins import DashboardRedirectUrlMixin
from django.urls.base import reverse
from edc_base.modeladmin.mixins import ModelAdminNextUrlRedirectMixin


@admin.register(MaternalRequisition)
class MaternalRequisitionAdmin(RequisitionAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    dashboard_type = 'maternal'
    form = MaternalRequisitionForm
    label_template_name = 'requisition_label'
    visit_attr = 'maternal_visit'
    visit_model = MaternalVisit
    panel_model = Panel

    def redirect_url(self, request, obj, post_url_continue=None):
        return request.GET.get('next')

#     def redirect_url(self, request, obj, post_url_continue=None):
#         url_name = request.GET.get(self.querystring_name)
#         subject_identifier = request.GET.get('subject_identifier')
#         appointment_id = request.GET.get('appointment_pk')
#         dashboard_url = reverse(url_name, kwargs={'appointment_pk': appointment_id, 'subject_identifier': subject_identifier})
#         show = 'show={}'.format(request.GET.get('show', None))
#         next_url = "{}?{}".format(dashboard_url, show)
#         return next_url

    def save_form(self, request, form, change):
        form.panel_name = request.GET.get('panel_name', None)
        return admin.ModelAdmin.save_form(self, request, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        panel_pk = request.GET.get('panel_name', 0)
        if db_field.name == 'panel_name':
            kwargs["queryset"] = self.panel_model.objects.filter(pk=panel_pk)
        visit_code = request.GET.get('visit_code', 0)
        subject_identifier = request.GET.get('subject_identifier')
        if db_field.name == 'maternal_visit':
            kwargs["queryset"] = MaternalVisit.objects.filter(
                appointment__visit_code=visit_code, appointment__subject_identifier=subject_identifier)
        return super(RequisitionAdminMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)
