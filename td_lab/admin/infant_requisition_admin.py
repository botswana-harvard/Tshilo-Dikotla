from copy import copy

from django.contrib import admin

from lab_requisition.admin import RequisitionAdminMixin

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin
from tshilo_dikotla.constants import INFANT
from td_infant.models import InfantVisit

from ..forms import InfantRequisitionForm
from ..models import InfantRequisition, Panel


class InfantRequisitionAdmin(RequisitionAdminMixin, MembershipBaseModelAdmin):

    dashboard_type = INFANT
    form = InfantRequisitionForm
    label_template_name = 'requisition_label'
    visit_attr = 'infant_visit'
    visit_model = InfantVisit
    panel_model = Panel

    def get_fieldsets(self, request, obj=None):
        fields = copy(self.fields)
        other_reason_field = ['reason_not_drawn_other']
        try:
            panel = Panel.objects.get(id=request.GET.get('panel'))
            if panel.name in ['Rectal swab (Storage)']:
                try:
                    fields.remove(fields.index('estimated_volume'))
                except ValueError:
                    pass
        except self.panel_model.DoesNotExist:
            pass
        try:
            fields.remove(fields.index('test_code'))
        except ValueError:
            pass
        fields.insert(4, other_reason_field)
        return [(None, {'fields': fields})]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
            if request.GET.get('infant_visit'):
                kwargs["queryset"] = InfantVisit.objects.filter(
                    id=request.GET.get('infant_visit'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(InfantRequisition, InfantRequisitionAdmin)
