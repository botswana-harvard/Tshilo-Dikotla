from collections import OrderedDict
from django.contrib import admin

from edc_visit_tracking.admin import VisitAdminMixin
from edc_export.actions import export_as_csv_action

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin
from tshilo_dikotla.constants import INFANT
from td_lab.models import InfantRequisition

from ..forms import InfantVisitForm
from ..models import InfantVisit


class InfantVisitAdmin(VisitAdminMixin, MembershipBaseModelAdmin):

    form = InfantVisitForm
    dashboard_type = INFANT
    requisition_model = InfantRequisition
    visit_attr = 'infant_visit'

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Visits",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'appointment__registered_subject__subject_identifier',
                 'gender': 'appointment__registered_subject__gender',
                 'dob': 'appointment__registered_subject__dob',
                 'registered': 'appointment__registered_subject__registration_datetime',
                 'visit_datetime': 'infant_visit__report_datetime',
                 'visit_reason': 'infant_visit__reason',
                 'study_status': 'infant_visit__study_status',
                 'reason_missed': 'infant_visit__reason_missed',
                 'info_source': 'infant_visit__info_source',
                 'survival_status': 'infant_visit__survival_status',
                 'last_alive_date': 'infant_visit__last_alive_date',
                 'comments': 'infant_visit__comments'}),
        )]

admin.site.register(InfantVisit, InfantVisitAdmin)
