from django.contrib import admin

from td.models import RegisteredSubject

from td.admin_mixins import ModelAdminMixin

from ..forms import MaternalLabourDelForm, MaternalHivInterimHxForm
from ..models import MaternalLabourDel, MaternalHivInterimHx

from .base_maternal_model_admin import BaseMaternalModelAdmin
from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin


@admin.register(MaternalLabourDel)
class MaternalLabourDelAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    dashboard_type = 'maternal'
    form = MaternalLabourDelForm

    list_display = ('registered_subject',
                    'delivery_datetime',
                    'labour_hrs',
                    'delivery_hospital',
                    'valid_regiment_duration')

    list_filter = ('delivery_hospital',
                   'valid_regiment_duration')

    search_fields = ('registered_subject__subject_identifier', )
    readonly_fields = ('live_infants_to_register',)

    radio_fields = {'delivery_time_estimated': admin.VERTICAL,
                    'delivery_hospital': admin.VERTICAL,
                    'valid_regiment_duration': admin.VERTICAL,
                    'mode_delivery': admin.VERTICAL,
                    'csection_reason': admin.VERTICAL,
                    'csection_reason': admin.VERTICAL, }
    filter_horizontal = ('delivery_complications',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('subject_identifier'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(
                    subject_identifier=request.GET.get('subject_identifier', 0))
            else:
                self.readonly_fields = list(self.readonly_fields)
                # try:
                #    self.readonly_fields.index('registered_subject')
                # except ValueError:
                #    self.readonly_fields.append('registered_subject')
        return super(MaternalLabourDelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(MaternalHivInterimHx)
class MaternalHivInterimHxAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalHivInterimHxForm

    radio_fields = {'has_cd4': admin.VERTICAL,
                    'has_vl': admin.VERTICAL,
                    'vl_detectable': admin.VERTICAL}
