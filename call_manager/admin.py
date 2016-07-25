from django.contrib import admin
from django.contrib.admin.options import StackedInline

from simple_history.admin import SimpleHistoryAdmin

from edc_base.modeladmin.mixins import (
    ModelAdminAuditFieldsMixin,
    ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin, ModelAdminModelRedirectMixin)
from edc_call_manager.admin import (
    ModelAdminCallMixin, ModelAdminLogMixin, ModelAdminLogEntryMixin,
    ModelAdminLogEntryInlineMixin, call_manager_admin)

from .models import Call, Log, LogEntry


class BaseModelAdmin(ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin):
    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


class ModelAdminStackedInlineMixin(ModelAdminAuditFieldsMixin, StackedInline):
    pass


@admin.register(Call, site=call_manager_admin)
class CallAdmin(BaseModelAdmin, ModelAdminCallMixin, SimpleHistoryAdmin):
    pass
#     subject_app = 'td_maternal'
#     subject_model = 'maternalconsent'


class LogEntryInlineAdmin(ModelAdminLogEntryInlineMixin, ModelAdminStackedInlineMixin):

    model = LogEntry


@admin.register(Log, site=call_manager_admin)
class LogAdmin(BaseModelAdmin, ModelAdminModelRedirectMixin, ModelAdminLogMixin, SimpleHistoryAdmin):

    inlines = [LogEntryInlineAdmin]


@admin.register(LogEntry, site=call_manager_admin)
class LogEntryAdmin(BaseModelAdmin, ModelAdminLogEntryMixin, SimpleHistoryAdmin):

    pass
