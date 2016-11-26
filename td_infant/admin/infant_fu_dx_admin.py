from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin_mixins import TabularInlineMixin
from edc_export.actions import export_as_csv_action

from td.admin_mixins import ModelAdminMixin

from ..models import InfantFuDx, InfantFuDxItems
from ..forms import InfantFuDxItemsForm

from .admin_mixins import CrfModelAdminMixin


class InfantFuDxItemsInline(TabularInlineMixin, admin.TabularInline):

    model = InfantFuDxItems
    form = InfantFuDxItemsForm
    extra = 0


@admin.register(InfantFuDxItems)
class InfantFuDxItemsAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = InfantFuDxItemsForm

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Followup Diagnosis with diagnoses",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'infant_fu_dx__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'infant_fu_dx__infant_visit__appointment__registered_subject__gender',
                 'dob': 'infant_fu_dx__infant_visit__appointment__registered_subject__dob',
                 }),
        )]


@admin.register(InfantFuDx)
class InfantFuDxAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    inlines = [InfantFuDxItemsInline, ]

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Followup Diagnosis",
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
