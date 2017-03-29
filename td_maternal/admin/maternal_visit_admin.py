from django.contrib import admin
from copy import copy
from collections import OrderedDict

from edc_visit_tracking.admin import VisitAdminMixin
from edc_export.actions import export_as_csv_action

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin
from td_lab.models import MaternalRequisition

from ..forms import MaternalVisitForm
from ..models import MaternalVisit


class MaternalVisitAdmin(VisitAdminMixin, MembershipBaseModelAdmin):

    form = MaternalVisitForm
    visit_attr = 'maternal_visit'
    requisition_model = MaternalRequisition
    dashboard_type = 'maternal'

    def get_fieldsets(self, request, obj=None):
        fields = copy(self.fields)
        fields.remove('information_provider')
        fields.remove('information_provider_other')
        return [(None, {'fields': fields})]

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Visits",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'appointment__registered_subject__subject_identifier',
                 'gender': 'appointment__registered_subject__gender',
                 'dob': 'appointment__registered_subject__dob',
                 'registered': 'appointment__registered_subject__registration_datetime',
                 'visit_datetime': 'maternal_visit__report_datetime',
                 'visit_reason': 'maternal_visit__reason',
                 'study_status': 'maternal_visit__study_status',
                 'reason_missed': 'maternal_visit__reason_missed',
                 'info_source': 'maternal_visit__info_source',
                 'survival_status': 'maternal_visit__survival_status',
                 'last_alive_date': 'maternal_visit__last_alive_date',
                 'comments': 'maternal_visit__comments'}),
        )]

admin.site.register(MaternalVisit, MaternalVisitAdmin)
