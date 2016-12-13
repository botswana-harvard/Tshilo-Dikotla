from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..forms import InfantBirthExamForm
from ..models import InfantBirthExam

from .admin_mixins import CrfModelAdminMixin


@admin.register(InfantBirthExam)
class InfantBirthExamAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = InfantBirthExamForm

    list_display = (
        'infant_visit',
        'general_activity',
        'physical_exam_result',
        'resp_exam',
    )

    list_filter = (
        'general_activity',
        'abnormal_activity',
        'physical_exam_result',
    )

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
            description="CSV Export of Infant Birth Record: Exam",
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
