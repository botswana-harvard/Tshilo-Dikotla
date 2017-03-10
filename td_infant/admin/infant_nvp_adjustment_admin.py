from collections import OrderedDict
from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..forms import InfantNvpAdjustmentForm
from ..models import InfantNvpAdjustment

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantNvpAdjustmentAdmin(BaseInfantScheduleModelAdmin, admin.ModelAdmin):

    form = InfantNvpAdjustmentForm

    radio_fields = {
        'dose_adjustment': admin.VERTICAL,
        'dose_4_weeks': admin.VERTICAL}

    list_display = ('infant_visit', 'dose_adjustment', 'dose_4_weeks',)

    list_filter = ('dose_adjustment', 'dose_4_weeks',)

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant NVP Dispensing",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'registered_subject__gender',
                 'dob': 'infant_visit__appointment__registered_subject__dob',
                 'dose_adjustment': 'infant_nvp_dispensing__dose_adjustment',
                 'adjusted_dose': 'infant_nvp_dispensing__adjusted_dose',
                 'dose_4_weeks': 'infant_nvp_dispensing__dose_4_weeks',
                 'incomplete_dose': 'infant_nvp_dispensing__incomplete_dose',
                 }),
        )]
admin.site.register(InfantNvpAdjustment, InfantNvpAdjustmentAdmin)
