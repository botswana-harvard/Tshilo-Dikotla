from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..forms import InfantFuForm
from ..models import InfantVisit, InfantFu

from .admin_mixins import InfantScheduleModelModelAdminMixin


@admin.register(InfantFu)
class InfantFuAdmin(InfantScheduleModelModelAdminMixin, admin.ModelAdmin):
    form = InfantFuForm

    list_display = (
        'physical_assessment',
        'diarrhea_illness',
        'has_dx',
        'was_hospitalized',
        'days_hospitalized',
    )

    radio_fields = {
        'physical_assessment': admin.VERTICAL,
        'diarrhea_illness': admin.VERTICAL,
        'has_dx': admin.VERTICAL,
        'was_hospitalized': admin.VERTICAL,
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Followup",
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
