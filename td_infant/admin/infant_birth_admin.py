from collections import OrderedDict

from django.contrib import admin

from edc_registration.models import RegisteredSubject
from edc_export.actions import export_as_csv_action

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin
from td_maternal.models import MaternalLabourDel

from ..forms import InfantBirthForm
from ..models import InfantBirth


class InfantBirthAdmin(MembershipBaseModelAdmin):

    form = InfantBirthForm

    list_display = (
        'registered_subject',
        'maternal_labour_del',
        'report_datetime',
        'first_name',
        'initials',
        'dob',
        'gender',
    )

    search_fields = ['registered_subject__subject_identifier', ]

    list_display = ('report_datetime', 'first_name', 'maternal_labour_del')
    list_filter = ('gender',)
    radio_fields = {'gender': admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Birth",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified', 'registered_subject', 'first_name', 'initials', 'dob'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'registered_subject__subject_identifier',
                 'gender': 'registered_subject__gender',
                 'dob': 'registered_subject__dob',
                 }),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(
                    id__exact=request.GET.get('registered_subject', 0))
        if db_field.name == "maternal_labour_del":
            if request.GET.get('registered_subject'):
                maternal_subject_identifier = RegisteredSubject.objects.get(
                    id=request.GET.get('registered_subject')).relative_identifier
                kwargs["queryset"] = MaternalLabourDel.objects.filter(
                    registered_subject__subject_identifier=maternal_subject_identifier)
        return super(InfantBirthAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantBirth, InfantBirthAdmin)
