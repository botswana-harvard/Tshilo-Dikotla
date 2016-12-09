from django.contrib import admin

from ..admin_site import td_maternal_admin
from ..forms import MaternalLocatorForm
from ..models import MaternalLocator

from td.admin_mixins import ModelAdminMixin
from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin


@admin.register(MaternalLocator, site=td_maternal_admin)
class MaternalLocatorAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    form = MaternalLocatorForm

    fields = ('subject_identifier',
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

    list_display = ('care_clinic',
                    'caretaker_name',
                    'caretaker_cell',
                    'caretaker_tel')
    list_filter = ('care_clinic', )
    search_fields = ('care_clinic', )
    radio_fields = {"home_visit_permission": admin.VERTICAL,
                    "may_follow_up": admin.VERTICAL,
                    "may_call_work": admin.VERTICAL,
                    "may_contact_someone": admin.VERTICAL,
                    'has_caretaker': admin.VERTICAL, }

    actions = []  # do not allow export to CSV
