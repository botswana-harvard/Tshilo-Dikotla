from django.contrib import admin

from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin, CareTakerFieldsAdminMixin

from tshilo_dikotla.admin_mixins import ModelAdminMixin
from tshilo_dikotla.constants import INFANT

from ..forms import InfantVisitForm
from ..models import InfantVisit


@admin.register(InfantVisit)
class InfantVisitAdmin(VisitModelAdminMixin, CareTakerFieldsAdminMixin, ModelAdminMixin):

    form = InfantVisitForm
    visit_attr = 'infant_visit'
    dashboard_type = INFANT
    # requisition_model = InfantRequisition  # ??
