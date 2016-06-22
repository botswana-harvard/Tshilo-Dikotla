from django.contrib import admin

from edc_visit_tracking.admin import VisitAdminMixin

from tshilo_dikotla.apps.td.base_model_admin import MembershipBaseModelAdmin
from tshilo_dikotla.apps.td.constants import INFANT
from tshilo_dikotla.apps.td_lab.models import InfantRequisition

from ..forms import InfantVisitForm
from ..models import InfantVisit


class InfantVisitAdmin(VisitAdminMixin, MembershipBaseModelAdmin):

    form = InfantVisitForm
    dashboard_type = INFANT
    requisition_model = InfantRequisition
    visit_attr = 'infant_visit'

admin.site.register(InfantVisit, InfantVisitAdmin)
