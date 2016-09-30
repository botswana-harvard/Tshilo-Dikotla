from copy import copy

from django.contrib import admin

from edc_lab.requisition.admin import RequisitionAdminMixin

from td_maternal.models import MaternalVisit

from ..forms import MaternalRequisitionForm
from ..models import MaternalRequisition, Panel
from tshilo_dikotla.admin_mixins import DashboardRedirectUrlMixin


@admin.register(MaternalRequisition)
class MaternalRequisitionAdmin(RequisitionAdminMixin, DashboardRedirectUrlMixin, admin.ModelAdmin):

    dashboard_type = 'maternal'
    form = MaternalRequisitionForm
    label_template_name = 'requisition_label'
    visit_attr = 'maternal_visit'
    visit_model = MaternalVisit
    panel_model = Panel
