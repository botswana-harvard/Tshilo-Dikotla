from copy import copy

from django.contrib import admin

from edc_lab.requisition.admin import RequisitionAdminMixin

from tshilo_dikotla.admin_mixins import EdcBaseModelAdminMixin
from tshilo_dikotla.constants import INFANT
from td_infant.models import InfantVisit

from ..forms import InfantRequisitionForm
from ..models import InfantRequisition, Panel


@admin.register(InfantRequisition)
class InfantRequisitionAdmin(RequisitionAdminMixin, EdcBaseModelAdminMixin, admin.ModelAdmin):

    dashboard_type = INFANT
    form = InfantRequisitionForm
    label_template_name = 'requisition_label'
    visit_attr = 'infant_visit'
    visit_model = InfantVisit
    panel_model = Panel
