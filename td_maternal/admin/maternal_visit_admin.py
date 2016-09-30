from django.contrib import admin
from copy import copy

from edc_visit_tracking.admin import VisitAdminMixin

from tshilo_dikotla.admin_mixins import EdcBaseModelAdminMixin
from td_lab.models import MaternalRequisition

from ..forms import MaternalVisitForm
from ..models import MaternalVisit


@admin.register(MaternalVisit)
class MaternalVisitAdmin(VisitAdminMixin, EdcBaseModelAdminMixin, admin.ModelAdmin):

    form = MaternalVisitForm
    visit_attr = 'maternal_visit'
    requisition_model = MaternalRequisition
    dashboard_type = 'maternal'

    def get_fieldsets(self, request, obj=None):
        fields = copy(self.fields)
        fields.remove('information_provider')
        fields.remove('information_provider_other')
        return [(None, {'fields': fields})]
