from django.contrib import admin
from collections import OrderedDict

from td_registration.models import RegisteredSubject
from edc_export.actions import export_as_csv_action

from tshilo_dikotla.admin_mixins import EdcBaseModelAdminMixin

from ..forms import AntenatalVisitMembershipForm
from ..models import AntenatalVisitMembership


@admin.register(AntenatalVisitMembership)
class AntenataVisitMembershipAdmin(EdcBaseModelAdminMixin, admin.ModelAdmin):

    dashboard_type = 'maternal'
    form = AntenatalVisitMembershipForm

    radio_fields = {'antenatal_visits': admin.VERTICAL}

    list_display = ('registered_subject', 'report_datetime', 'antenatal_visits')

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
            else:
                self.readonly_fields = list(self.readonly_fields)
                try:
                    self.readonly_fields.index('registered_subject')
                except ValueError:
                    self.readonly_fields.append('registered_subject')
        return super(AntenataVisitMembershipAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
