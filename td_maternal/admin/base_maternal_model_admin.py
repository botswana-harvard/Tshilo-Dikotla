from collections import OrderedDict

from edc_export.actions import export_as_csv_action

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin
from ..models import MaternalVisit


class BaseMaternalModelAdmin(MembershipBaseModelAdmin):

    dashboard_type = 'maternal'
    visit_model_name = 'maternalvisit'

    search_fields = [
        'maternal_visit__appointment__registered_subject__subject_identifier',
        'maternal_visit__appointment__registered_subject__initials', ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
            if request.GET.get('maternal_visit'):
                kwargs["queryset"] = MaternalVisit.objects.filter(
                    id=request.GET.get('maternal_visit'))
        return super(BaseMaternalModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    actions = [
        export_as_csv_action(
            description="Export to CSV file",
            fields=[],
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
