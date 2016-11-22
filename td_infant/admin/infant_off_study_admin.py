from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from tshilo_dikotla.admin_mixins import EdcBaseModelAdminMixin
from tshilo_dikotla.constants import INFANT

from ..forms import InfantOffStudyForm
from ..models import InfantOffStudy


@admin.register(InfantOffStudy)
class InfantOffStudyAdmin(EdcBaseModelAdminMixin, admin.ModelAdmin):

    form = InfantOffStudyForm
    dashboard_type = INFANT
    visit_model_name = 'infantvisit'

    fields = (
        'infant_visit',
        'report_datetime',
        'offstudy_date',
        'reason',
        'reason_other',
        'comment',
    )

    list_display = (
        'infant_visit',
#         'offstudy_date',
        'reason')

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Off Study",
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
