from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseTabularInline
from edc_export.actions import export_as_csv_action

from tshilo_dikotla.base_model_admin import BaseModelAdmin

from ..models import InfantFuDx, InfantFuDxItems
from ..forms import InfantFuDxItemsForm

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantFuDxItemsInline(BaseTabularInline):

    model = InfantFuDxItems
    form = InfantFuDxItemsForm
    extra = 0


class InfantFuDxItemsAdmin(BaseModelAdmin):
    form = InfantFuDxItemsForm

    search_fields = [
        'infant_fu_dx__infant_visit__appointment__registered_subject__subject_identifier',
        'infant_fu_dx__infant_visit__appointment__registered_subject__initials', ]

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

admin.site.register(InfantFuDxItems, InfantFuDxItemsAdmin)


class InfantFuDxAdmin(BaseInfantScheduleModelAdmin):

    inlines = [InfantFuDxItemsInline, ]

admin.site.register(InfantFuDx, InfantFuDxAdmin)
