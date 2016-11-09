from django.contrib import admin
from copy import copy

from django.core.urlresolvers import reverse
from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin

from tshilo_dikotla.admin_mixins import EdcBaseModelAdminMixin
from td_lab.models import MaternalRequisition

from ..forms import MaternalVisitForm
from ..models import MaternalVisit
from edc_base.modeladmin.mixins import ModelAdminNextUrlRedirectMixin
from td_appointment.models import Appointment


@admin.register(MaternalVisit)
class MaternalVisitAdmin(VisitModelAdminMixin, EdcBaseModelAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    form = MaternalVisitForm
    visit_attr = 'maternal_visit'
    requisition_model = MaternalRequisition
    dashboard_type = 'maternal'

    def redirect_url(self, request, obj, post_url_continue=None):
        args = request.GET.dict()
        args.pop(self.querystring_name)
        args.pop('visit_code')
        redirect_url = super(ModelAdminNextUrlRedirectMixin, self).redirect_url(
            request, obj, post_url_continue)
        if request.GET.get(self.querystring_name):
            url_name = request.GET.get(self.querystring_name)
            return reverse(url_name, args=[element for element in args.values()])
        return redirect_url

    def get_fields(self, request, obj=None):
        fields = admin.ModelAdmin.get_fields(self, request, obj=obj)
        if fields:
            fields.remove('information_provider')
            fields.remove('information_provider_other')
        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'appointment' and request.GET.get('subject_identifier'):
            kwargs["queryset"] = Appointment.objects.filter(subject_identifier=request.GET.get('subject_identifier'),
                                                            visit_code=request.GET.get('visit_code'))

        return super(MaternalVisitAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
