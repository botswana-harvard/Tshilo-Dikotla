from django.contrib import admin

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin

from ..models import Receive


class ReceiveAdmin(MembershipBaseModelAdmin):

    date_hierarchy = 'receive_datetime'

    list_display = ("receive_identifier", "requisition", "receive_datetime", "drawn_datetime",
                    'registered_subject', 'subject_type', 'created', 'modified', 'import_datetime')

    search_fields = ('registered_subject__subject_identifier', 'subject_type',
                     "receive_identifier", "requisition_identifier",)

    list_filter = ('created', "receive_datetime", "drawn_datetime", 'modified', 'import_datetime', )

    list_per_page = 15

    def get_readonly_fields(self, request, obj):
        return (['receive_identifier', 'requisition_model_name', 'clinician_initials'] +
                [field.name for field in obj._meta.fields if field.editable])

admin.site.register(Receive, ReceiveAdmin)
