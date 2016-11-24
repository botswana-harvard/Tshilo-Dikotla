from django.contrib import admin
from django.contrib.admin.options import StackedInline

from simple_history.admin import SimpleHistoryAdmin

from edc_base.modeladmin_mixins import (
    ModelAdminAuditFieldsMixin,
    ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin, ModelAdminModelRedirectMixin)
from edc_call_manager.admin import (
    ModelAdminCallMixin, ModelAdminLogMixin, ModelAdminLogEntryMixin,
    ModelAdminLogEntryInlineMixin)

from .models import Call, Log, LogEntry


class BaseModelAdmin(ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin):
    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


class ModelAdminStackedInlineMixin(ModelAdminAuditFieldsMixin, StackedInline):
    pass


class CallAdmin(BaseModelAdmin, ModelAdminCallMixin, SimpleHistoryAdmin):
    subject_app = 'td_maternal'
    subject_model = 'antenatalenrollment'

    readonly_fields = (
        'call_attempts',
        'call_status',
    )

    mixin_fields = (
        'call_attempts',
        'scheduled',
        'call_status',
    )

    mixin_list_filter = (
        'call_status',
        'call_attempts',
        'scheduled',
        'modified',
        'hostname_created',
        'user_created',
    )

    mixin_list_display = (
        'subject_identifier',
        'call_button',
        'call_attempts',
        'call_outcome',
        'scheduled',
        'label',
        'first_name',
        'initials',
        'user_created',
    )

admin.site.register(Call, CallAdmin)


class LogEntryInlineAdmin(ModelAdminLogEntryInlineMixin, ModelAdminStackedInlineMixin):

    model = LogEntry


@admin.register(Log)
class LogAdmin(BaseModelAdmin, ModelAdminModelRedirectMixin, ModelAdminLogMixin, SimpleHistoryAdmin):
    pass


class LogEntryAdmin(BaseModelAdmin, ModelAdminLogEntryMixin, SimpleHistoryAdmin):
    pass
admin.site.register(LogEntry, LogEntryAdmin)
