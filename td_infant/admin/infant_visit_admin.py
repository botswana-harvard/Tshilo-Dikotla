from django.contrib import admin

from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin

from tshilo_dikotla.admin_mixins import DashboardRedirectUrlMixin, EdcBaseModelAdminMixin
from tshilo_dikotla.constants import INFANT
from td_lab.models import InfantRequisition

from ..forms import InfantVisitForm
from ..models import InfantVisit


@admin.register(InfantVisit)
class InfantVisitAdmin(VisitModelAdminMixin, EdcBaseModelAdminMixin, admin.ModelAdmin):

    form = InfantVisitForm
    visit_attr = 'infant_visit'
    dashboard_type = INFANT
    requisition_model = InfantRequisition  # ??
