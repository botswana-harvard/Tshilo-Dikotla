from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseTabularInline
from edc_export.actions import export_as_csv_action

from ..models import InfantBirthFeedingVaccine, InfantVaccines
from ..forms import InfantVaccinesForm, InfantBirthFeedinVaccineForm

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantVaccinesInline(BaseTabularInline):

    model = InfantVaccines
    form = InfantVaccinesForm
    extra = 0


class InfantBirthFeedingVaccineAdmin(BaseInfantScheduleModelAdmin):
    form = InfantBirthFeedinVaccineForm

    list_display = ('feeding_after_delivery',)

    list_filter = ('feeding_after_delivery',)

    inlines = [InfantVaccinesInline]

    radio_fields = {'feeding_after_delivery': admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Birth Feeding & Vaccination",
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

admin.site.register(InfantBirthFeedingVaccine, InfantBirthFeedingVaccineAdmin)


class InfantVaccinesAdmin(admin.ModelAdmin):
    form = InfantVaccinesForm
admin.site.register(InfantVaccines, InfantVaccinesAdmin)
