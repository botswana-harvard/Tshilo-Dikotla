from django.contrib import admin
from collections import OrderedDict

from edc_registration.models import RegisteredSubject
from edc_export.actions import export_as_csv_action

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin

from ..forms import AntenatalVisitMembershipForm
from ..models import AntenatalVisitMembership


class AntenataVisitMembershipAdmin(MembershipBaseModelAdmin):

    dashboard_type = 'maternal'
    form = AntenatalVisitMembershipForm

    search_fields = ['registered_subject__subject_identifier',
                     'registered_subject__initials']

    radio_fields = {'antenatal_visits': admin.VERTICAL}

    list_display = (
        'registered_subject', 'report_datetime', 'antenatal_visits')

    actions = [
        export_as_csv_action(
            description="CSV Export of Antenatal Enrollment",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'registered_subject__subject_identifier',
                 'gender': 'registered_subject__gender',
                 'dob': 'registered_subject__dob',
                 'registered': 'registered_subject__registration_datetime'}),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(
                    id__exact=request.GET.get('registered_subject', 0))
        return super(AntenataVisitMembershipAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(AntenatalVisitMembership, AntenataVisitMembershipAdmin)
