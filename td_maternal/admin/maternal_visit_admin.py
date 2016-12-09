from django.contrib import admin

from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin

from td.models import Appointment
from td_lab.models import MaternalRequisition

from ..admin_site import td_maternal_admin
from ..forms import MaternalVisitForm
from ..models import MaternalVisit

from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(MaternalVisit, site=td_maternal_admin)
class MaternalVisitAdmin(VisitModelAdminMixin, BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalVisitForm
    visit_attr = 'maternal_visit'
    requisition_model = MaternalRequisition
    dashboard_type = 'maternal'

    def get_fields(self, request, obj=None):
        fields = admin.ModelAdmin.get_fields(self, request, obj=obj)
        if fields:
            try:
                fields.remove(fields.index('information_provider'))
            except ValueError:
                pass
            try:
                fields.remove(fields.index('information_provider_other'))
            except ValueError:
                pass
        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'appointment' and request.GET.get('subject_identifier'):
            kwargs["queryset"] = Appointment.objects.filter(subject_identifier=request.GET.get('subject_identifier'),
                                                            visit_code=request.GET.get('visit_code'))

        return super(MaternalVisitAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
