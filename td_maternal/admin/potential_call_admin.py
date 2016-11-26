from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from edc_base.modeladmin_mixins import (ModelAdminChangelistModelButtonMixin, ModelAdminRedirectMixin,
                                        ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
                                        ModelAdminAuditFieldsMixin)
from edc_call_manager.models import Call

from ..models import PotentialCall


class BaseModelAdmin(ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
                     ModelAdminAuditFieldsMixin,
                     SimpleHistoryAdmin):
    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


@admin.register(PotentialCall)
class PotentialCallAdmin(ModelAdminRedirectMixin, ModelAdminChangelistModelButtonMixin,
                         BaseModelAdmin):

    fields = ['subject_identifier', 'approximate_date', 'identity', 'first_name', 'last_name',
              'visit_code', 'dob']

    list_display = ['subject_identifier', 'identity', 'contacted', 'first_name', 'last_name',
                    'approximate_date', 'visit_code', 'dob', 'jum_to_call_button']

    list_filter = ['subject_identifier', 'identity', 'contacted', 'approximate_date', 'visit_code']

    radio_fields = {
        'gender': admin.VERTICAL
    }

    search_fields = ['identity', 'subject_identifier', 'visit_code', 'first_name']

    readonly_fields = ['subject_identifier', 'identity', 'visit_code', 'first_name', 'last_name',
                       'initials', 'dob']

    def jum_to_call_button(self, obj):
        reverse_args = None
        try:
            call = Call.objects.get(potential_call=obj)
            reverse_args = (call.pk, )
        except Call.DoesNotExist:
            pass
        return self.changelist_model_button(
            'call_manager', 'call', reverse_args=reverse_args,
            change_label='goto_call')
    jum_to_call_button.short_description = 'go to call'
