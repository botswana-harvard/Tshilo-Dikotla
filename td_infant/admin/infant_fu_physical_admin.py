from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..forms import InfantFuPhysicalForm
from ..models import InfantFuPhysical

from .admin_mixins import InfantScheduleModelModelAdminMixin


@admin.register(InfantFuPhysical)
class InfantFuPhysicalAdmin(InfantScheduleModelModelAdminMixin, admin.ModelAdmin):
    form = InfantFuPhysicalForm

    radio_fields = {
        'general_activity': admin.VERTICAL,
        'physical_exam_result': admin.VERTICAL,
        'heent_exam': admin.VERTICAL,
        'resp_exam': admin.VERTICAL,
        'cardiac_exam': admin.VERTICAL,
        'abdominal_exam': admin.VERTICAL,
        'skin_exam': admin.VERTICAL,
        'neurologic_exam': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Followup Physical",
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
