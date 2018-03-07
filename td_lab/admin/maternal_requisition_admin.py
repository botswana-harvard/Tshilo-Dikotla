from copy import copy

from django.contrib import admin

from lab_requisition.admin import RequisitionAdminMixin

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin
from td_maternal.models import MaternalVisit

from ..forms import MaternalRequisitionForm
from ..models import MaternalRequisition, Panel


class MaternalRequisitionAdmin(RequisitionAdminMixin, MembershipBaseModelAdmin):

    dashboard_type = 'maternal'
    form = MaternalRequisitionForm
    label_template_name = 'requisition_label'
    visit_attr = 'maternal_visit'
    visit_model = MaternalVisit
    panel_model = Panel

    def get_fieldsets(self, request, obj=None):
        fields = copy(self.fields)
        other_reason_field = ['reason_not_drawn_other']
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
        fields.insert(4, other_reason_field)
        return [(None, {'fields': fields})]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
            if request.GET.get('maternal_visit'):
                kwargs["queryset"] = MaternalVisit.objects.filter(
                    id=request.GET.get('maternal_visit'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(MaternalRequisition, MaternalRequisitionAdmin)
