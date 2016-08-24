from copy import copy

from django.contrib import admin

from lab_requisition.admin import RequisitionAdminMixin

from td_maternal.models import MaternalVisit

from ..forms import MaternalRequisitionForm
from ..models import MaternalRequisition, Panel
from tshilo_dikotla.admin_mixins import DashboardRedirectUrlMixin


class MaternalRequisitionAdmin(RequisitionAdminMixin, DashboardRedirectUrlMixin, admin.ModelAdmin):

    dashboard_type = 'maternal'
    form = MaternalRequisitionForm
    label_template_name = 'requisition_label'
    visit_attr = 'maternal_visit'
    visit_model = MaternalVisit
    panel_model = Panel

    def get_fieldsets(self, request, obj=None):
        fields = copy(self.fields)
        panel_names = [
            'Vaginal swab (Storage)',
            'Rectal swab (Storage)',
            'Skin Swab (Storage)',
            'Vaginal STI Swab (Storage)']
        try:
            panel = self.panel_model.objects.get(id=request.GET.get('panel'))
            if panel.name in panel_names:
                try:
                    fields.remove('estimated_volume')
                except ValueError:
                    pass
        except self.panel_model.DoesNotExist:
            pass
        return [(None, {'fields': fields})]

admin.site.register(MaternalRequisition, MaternalRequisitionAdmin)
