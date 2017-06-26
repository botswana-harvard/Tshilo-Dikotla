from django.contrib import admin
from collections import OrderedDict

from edc_export.actions import export_as_csv_action

from ..forms import MaternalDiagnosesForm
from ..models import MaternalDiagnoses
from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalDiagnosesAdmin(BaseMaternalModelAdmin):

    form = MaternalDiagnosesForm
    list_display = ('maternal_visit', 'new_diagnoses', 'has_who_dx')
    list_filter = ('new_diagnoses', 'has_who_dx')
    radio_fields = {'new_diagnoses': admin.VERTICAL,
                    'has_who_dx': admin.VERTICAL}
    filter_horizontal = ('who', 'diagnoses')

    actions = [
        export_as_csv_action(
            description="Export to CSV file",
            fields=[
                'new_diagnoses', 'diagnoses', 'diagnoses_other', 'has_who_dx',
                'who__short_name'],
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

admin.site.register(MaternalDiagnoses, MaternalDiagnosesAdmin)
