from django.contrib import admin
from collections import OrderedDict

from edc_registration.models import RegisteredSubject
from edc_export.actions import export_as_csv_action

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin

from ..forms import MaternalLabourDelForm, MaternalHivInterimHxForm
from ..models import MaternalLabourDel, MaternalHivInterimHx

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalLabourDelAdmin(MembershipBaseModelAdmin):

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
    # readonly_fields = ('live_infants_to_register',)

    radio_fields = {'delivery_time_estimated': admin.VERTICAL,
                    'delivery_hospital': admin.VERTICAL,
                    'valid_regiment_duration': admin.VERTICAL,
                    'mode_delivery': admin.VERTICAL,
                    'csection_reason': admin.VERTICAL,
                    'csection_reason': admin.VERTICAL, }
    filter_horizontal = ('delivery_complications',)

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Deliveries",
            fields=[
                'delivery_datetime', 'delivery_time_estimated', 'delivery_hospital',
                'delivery_hospital_other', 'labour_hrs', 'mode_delivery',
                'mode_delivery_other', 'csection_reason', 'csection_reason_other',
                'delivery_complications', 'delivery_complications_other',
                'live_infants_to_register', 'still_births', 'valid_regiment_duration',
                'arv_initiation_date', 'delivery_comment'
            ],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified', 'exported', 'exported_datetime', 'export_change_type', 'export_uuid'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'registered_subject__subject_identifier',
                 'gender': 'registered_subject__gender',
                 'dob': 'registered_subject__dob',
                 'registered': 'registered_subject__registration_datetime'}),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(
                    id__exact=request.GET.get('registered_subject', 0))
            else:
                self.readonly_fields = list(self.readonly_fields)
#                 try:
#                     self.readonly_fields.index('registered_subject')
#                 except ValueError:
#                     self.readonly_fields.append('registered_subject')
        return super(MaternalLabourDelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalLabourDel, MaternalLabourDelAdmin)


class MaternalHivInterimHxAdmin(BaseMaternalModelAdmin):

    form = MaternalHivInterimHxForm

    radio_fields = {'has_cd4': admin.VERTICAL,
                    'has_vl': admin.VERTICAL,
                    'vl_detectable': admin.VERTICAL}

admin.site.register(MaternalHivInterimHx, MaternalHivInterimHxAdmin)
