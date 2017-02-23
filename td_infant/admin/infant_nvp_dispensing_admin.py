from collections import OrderedDict
from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..forms import InfantNvpDispensingForm
from ..models import InfantNvpDispensing

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantNvpDispensingAdmin(BaseInfantScheduleModelAdmin, admin.ModelAdmin):

    form = InfantNvpDispensingForm

    radio_fields = {'nvp_prophylaxis': admin.VERTICAL,
                    'azt_prophylaxis': admin.VERTICAL,
                    'medication_instructions': admin.VERTICAL,
                    'correct_dose': admin.VERTICAL}

    list_display = ('infant_visit', 'nvp_prophylaxis', 'azt_prophylaxis', 'medication_instructions',)

    list_filter = ('nvp_prophylaxis', 'azt_prophylaxis', 'correct_dose',)

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
                 'nvp_prophylaxis': 'infant_nvp_dispensing__nvp_prophylaxis',
                 'reason_not_given': 'infant_nvp_dispensing__reason_not_given',
                 'azt_prophylaxis': 'infant_nvp_dispensing__azt_prophylaxis',
                 'azt_dose_given': 'infant_nvp_dispensing__azt_dose_given',
                 'nvp_admin_date': 'infant_nvp_dispensing__nvp_admin_date',
                 'medication_instructions': 'infant_nvp_dispensing__medication_instructions',
                 'dose_admin_infant': 'infant_nvp_dispensing__dose_admin_infant',
                 'correct_dose': 'infant_nvp_dispensing__correct_dose',
                 'corrected_dose': 'infant_nvp_dispensing__corrected_dose'
                 }),
        )]
admin.site.register(InfantNvpDispensing, InfantNvpDispensingAdmin)
