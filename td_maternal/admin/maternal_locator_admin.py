from edc_registration.models import RegisteredSubject

from django.contrib import admin

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin, BaseModelAdmin

from ..forms import MaternalLocatorForm
from ..models import MaternalLocator


class MaternalLocatorAdmin(MembershipBaseModelAdmin, BaseModelAdmin):

    form = MaternalLocatorForm

    fields = (
        'registered_subject',
        'report_datetime',
        'date_signed',
        'mail_address',
        'care_clinic',
        'home_visit_permission',
        'physical_address',
        'may_follow_up',
        'subject_cell',
        'subject_cell_alt',
        'subject_phone',
        'subject_phone_alt',
        'may_call_work',
        'subject_work_place',
        'subject_work_phone',
        'may_contact_someone',
        'contact_name',
        'contact_rel',
        'contact_physical_address',
        'contact_cell',
        'contact_phone',
        'has_caretaker',
        'caretaker_name',
        'caretaker_cell',
        'caretaker_tel')

    list_display = (
        'care_clinic',
        'caretaker_name',
        'caretaker_cell',
        'caretaker_tel')
    list_filter = ('care_clinic', )
    search_fields = ('care_clinic', 'registered_subject__subject_identifier',
                     'registered_subject__identity')

    radio_fields = {"home_visit_permission": admin.VERTICAL,
                    "may_follow_up": admin.VERTICAL,
                    "may_call_work": admin.VERTICAL,
                    "may_contact_someone": admin.VERTICAL,
                    'has_caretaker': admin.VERTICAL, }

    actions = []  # do not allow export to CSV

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(
                    id__exact=request.GET.get('registered_subject', 0))
        return super(MaternalLocatorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(MaternalLocator, MaternalLocatorAdmin)
