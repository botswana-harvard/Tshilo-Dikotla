from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..models import InfantBirthArv, InfantVisit

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantBirthArvAdmin(BaseInfantScheduleModelAdmin):

    list_display = (
        'infant_visit', 'azt_after_birth',
        'azt_dose_date', 'azt_additional_dose',
        'sdnvp_after_birth',)

    list_filter = ('azt_after_birth', 'azt_dose_date', 'azt_additional_dose', 'sdnvp_after_birth',)

    radio_fields = {
        'azt_after_birth': admin.VERTICAL,
        'azt_additional_dose': admin.VERTICAL,
        'sdnvp_after_birth': admin.VERTICAL,
        'azt_discharge_supply': admin.VERTICAL,
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Birth Record: ARV",
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(InfantBirthArvAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantBirthArv, InfantBirthArvAdmin)
