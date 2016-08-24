from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.mixins import TabularInlineMixin
from edc_export.actions import export_as_csv_action

from tshilo_dikotla.admin_mixins import EdcBaseModelAdminMixin, DashboardRedirectUrlMixin

from ..forms import InfantFuNewMedItemsForm, InfantFuNewMedForm
from ..models import InfantFuNewMed, InfantFuNewMedItems

from .admin_mixins import InfantScheduleModelModelAdminMixin


class InfantFuNewMedItemsInline(TabularInlineMixin, admin.TabularInline):

    model = InfantFuNewMedItems
    form = InfantFuNewMedItemsForm
    extra = 0


@admin.register(InfantFuNewMedItems)
class InfantFuNewMedItemsAdmin(EdcBaseModelAdminMixin, DashboardRedirectUrlMixin, admin.ModelAdmin):

    form = InfantFuNewMedItemsForm

    actions = [
        export_as_csv_action(
            description="CSV Export of Followup New Medications with meds list",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'infant_fu_med__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'infant_fu_med__infant_visit__appointment__registered_subject__gender',
                 'dob': 'infant_fu_med__infant_visit__appointment__registered_subject__dob',
                 'new_medications': 'infant_fu_med__new_medications',
                 }),
        )]


@admin.register(InfantFuNewMed)
class InfantFuNewMedAdmin(InfantScheduleModelModelAdminMixin, admin.ModelAdmin):

    radio_fields = {'new_medications': admin.VERTICAL, }
    inlines = [InfantFuNewMedItemsInline, ]
    form = InfantFuNewMedForm

    actions = [
        export_as_csv_action(
            description="CSV Export of Followup New Medications",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'infant_visit__appointment__registered_subject__gender',
                 'dob': 'infant_visit__appointment__registered_subject__dob',
                 }),
        )]
