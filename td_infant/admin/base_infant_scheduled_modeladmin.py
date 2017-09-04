from collections import OrderedDict

from edc_export.actions import export_as_csv_action
from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin

from ..models import InfantVisit


class BaseInfantScheduleModelAdmin(MembershipBaseModelAdmin):

    search_fields = [
        'infant_visit__appointment__registered_subject__subject_identifier',
        'infant_visit__appointment__registered_subject__initials', ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
            if request.GET.get('infant_visit'):
                kwargs["queryset"] = InfantVisit.objects.filter(
                    id=request.GET.get('infant_visit'))
        return super(BaseInfantScheduleModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    actions = [
        export_as_csv_action(
            description="Export CSV file",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified', 'infant_visit'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'infant_visit__appointment__registered_subject__gender',
                 'dob': 'infant_visit__appointment__registered_subject__dob',
                 'registered': 'infant_visit__appointment__registered_subject__registration_datetime',
                 'visit_code': 'infant_visit__appointment__visit_definition__code',
                 'visit_reason': 'infant_visit__reason',
                 'visit_study_status': 'infant_visit__study_status'
                 }),
        )]
