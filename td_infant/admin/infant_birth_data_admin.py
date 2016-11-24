from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..forms import InfantBirthDataForm
from ..models import InfantBirthData

from .admin_mixins import CrfModelAdminMixin


@admin.register(InfantBirthData)
class InfantBirthDataAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = InfantBirthDataForm

    fields = (
        "infant_visit",
        "weight_kg",
        "infant_length",
        "head_circumference",
        "apgar_score",
        "apgar_score_min_1",
        "apgar_score_min_5",
        "apgar_score_min_10",
        "congenital_anomalities",
        "other_birth_info")

    radio_fields = {
        "apgar_score": admin.VERTICAL,
        "congenital_anomalities": admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Birth Record: Data",
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
