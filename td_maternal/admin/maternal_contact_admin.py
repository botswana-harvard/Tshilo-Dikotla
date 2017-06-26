from django.contrib import admin
from collections import OrderedDict

from edc_export.actions import export_as_csv_action

from edc_base.modeladmin.mixins import (ModelAdminRedirectMixin,
                                        ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
                                        ModelAdminAuditFieldsMixin)
from edc_registration.models import RegisteredSubject

from simple_history.admin import SimpleHistoryAdmin

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin, BaseModelAdmin
from td_maternal.models import MaternalContact
from django.contrib.admin.templatetags.admin_list import admin_actions

from ..forms import MaternalContactForm


class BaseModelAdmin(ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
                     ModelAdminAuditFieldsMixin,
                     SimpleHistoryAdmin):
    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


@admin.register(MaternalContact)
class MaternalContactAdmin(BaseModelAdmin):

    form = MaternalContactForm

    fields = [
        'registered_subject',
        'report_datetime',
        'contact_type',
        'contact_datetime',
        'call_reason',
        'call_reason_other',
        'contact_success',
        'contact_comment']

    list_display = [
        'registered_subject', 'contact_type',
        'contact_datetime', 'call_reason', 'contact_success']

    list_filter = ['contact_type', 'call_reason', 'contact_success']

    radio_fields = {
        'contact_type': admin.VERTICAL,
        'call_reason': admin.VERTICAL,
        'contact_success': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="Export to CSV file",
            fields=[],
            delimiter=',',
            exclude=['maternal_visit', 'user_created', 'user_modified', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'registered_subject__subject_identifier', }),
        )]

    search_fields = ['registered_subject__subject_identifier',
                     'contact_type', 'call_reason', 'contact_success']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            kwargs["queryset"] = RegisteredSubject.objects.filter(
                id__exact=request.GET.get('registered_subject'))
        return super(MaternalContactAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
