from collections import OrderedDict
from edc_export.actions import export_as_csv_action

from django.contrib import admin

from ..forms import MaternalPostPartumFuForm
from ..models import MaternalPostPartumFu
from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalPostPartumFuAdmin(BaseMaternalModelAdmin):

    form = MaternalPostPartumFuForm
    fields = ('maternal_visit',
              'report_datetime',
              'new_diagnoses',
              'diagnoses',
              'diagnoses_other',
              'hospitalized',
              'hospitalization_reason',
              'hospitalization_reason_other',
              'hospitalization_days',
              'has_who_dx',
              'who')
    list_display = ('maternal_visit', 'new_diagnoses', 'has_who_dx')
    list_filter = ('new_diagnoses', 'diagnoses', 'has_who_dx')
    radio_fields = {'new_diagnoses': admin.VERTICAL,
                    'hospitalized': admin.VERTICAL,
                    'has_who_dx': admin.VERTICAL}
    filter_horizontal = ('who', 'diagnoses', 'hospitalization_reason')

    actions = [
        export_as_csv_action(
            description="Export to CSV file",
            fields=['hospitalized', 'new_diagnoses',
                    'hospitalization_reason_other', 'hospitalization_days',
                    'diagnoses_other', 'has_who_dx'],
            delimiter=',',
            exclude=['maternal_visit', 'user_created', 'user_modified', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'maternal_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'maternal_visit__appointment__registered_subject__gender',
                 'dob': 'maternal_visit__appointment__registered_subject__dob',
                 'screened': 'maternal_visit__appointment__registered_subject__screening_datetime',
                 'registered': 'maternal_visit__appointment__registered_subject__registration_datetime',
                 'visit_code': 'maternal_visit__appointment__visit_definition__code',
                 'visit_reason': 'maternal_visit__reason',
                 'visit_study_status': 'maternal_visit__study_status'}),
        )]


admin.site.register(MaternalPostPartumFu, MaternalPostPartumFuAdmin)
