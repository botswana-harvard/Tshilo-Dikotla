from django.contrib import admin
from collections import OrderedDict

from edc_export.actions import export_as_csv_action

from ..forms import MaternalMedicalHistoryForm
from ..models import MaternalMedicalHistory
from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalMedicalHistoryAdmin(BaseMaternalModelAdmin):

    form = MaternalMedicalHistoryForm
#     fields = ('maternal_visit',
#               'chronic_since',
# #               'chronic',
#               'chronic_other',
#               'who_diagnosis',
# #               'who',
#     )
    list_display = ('maternal_visit', 'chronic_since', 'sero_posetive', 'date_hiv_diagnosis', 'perinataly_infected',
                    'lowest_cd4_known', 'cd4_count', 'cd4_date')
    list_filter = (
        'chronic_since', 'sero_posetive', 'date_hiv_diagnosis', 'perinataly_infected')
    radio_fields = {'chronic_since': admin.VERTICAL,
                    'who_diagnosis': admin.VERTICAL,
                    'sero_posetive': admin.VERTICAL,
                    'perinataly_infected': admin.VERTICAL,
                    'know_hiv_status': admin.VERTICAL,
                    'lowest_cd4_known': admin.VERTICAL,
                    'is_date_estimated': admin.VERTICAL}
    filter_horizontal = (
        'who', 'mother_chronic', 'father_chronic', 'mother_medications')

    actions = [
        export_as_csv_action(
            description="Export to CSV file",
            fields=['chronic_since', 'who_diagnosis', 'who__short_name',
                    'mother_chronic__name', 'mother_chronic_other', 'father_chronic__name',
                    'father_chronic_other', 'mother_medications__name', 'mother_medications_other',
                    'sero_posetive', 'date_hiv_diagnosis', 'perinataly_infected',
                    'know_hiv_status', 'lowest_cd4_known', 'cd4_count', 'cd4_date',
                    'is_date_estimated', ],
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

admin.site.register(MaternalMedicalHistory, MaternalMedicalHistoryAdmin)
