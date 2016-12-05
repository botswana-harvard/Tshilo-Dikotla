from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from td.admin_mixins import ModelAdminMixin

from ..forms import InfantBirthForm
from ..models import InfantBirth


@admin.register(InfantBirth)
class InfantBirthAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InfantBirthForm

    list_display = (
        'delivery_reference',
        'report_datetime',
        'first_name',
        'initials',
        'dob',
        'gender',
    )

    list_filter = ('gender', 'delivery_reference')
    radio_fields = {'gender': admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Birth",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'subject_identifier',
                 'gender': 'gender',
                 'dob': 'dob',
                 }),
        )]
