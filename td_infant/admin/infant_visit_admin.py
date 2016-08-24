from django.contrib import admin

from edc_visit_tracking.admin import VisitAdminMixin

from tshilo_dikotla.admin_mixins import DashboardRedirectUrlMixin, EdcBaseModelAdminMixin
from tshilo_dikotla.constants import INFANT
from td_lab.models import InfantRequisition

from ..forms import InfantVisitForm
from ..models import InfantVisit


@admin.register(InfantVisit)
class InfantVisitAdmin(VisitAdminMixin, EdcBaseModelAdminMixin, DashboardRedirectUrlMixin, admin.ModelAdmin):

    form = InfantVisitForm
    dashboard_type = INFANT
    requisition_model = InfantRequisition  # ??
    visit_attr = 'infant_visit'
