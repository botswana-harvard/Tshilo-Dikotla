from django.contrib import admin

from edc_base.modeladmin.mixins import (ModelAdminChangelistModelButtonMixin, ModelAdminRedirectMixin,
                                        ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
                                        ModelAdminAuditFieldsMixin)
from simple_history.admin import SimpleHistoryAdmin

from td_maternal.models import PotentialCall, MaternalConsent


class BaseModelAdmin(ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
                     ModelAdminAuditFieldsMixin,
                     SimpleHistoryAdmin):
    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


@admin.register(PotentialCall)
class PotentialCallAdmin(ModelAdminRedirectMixin, ModelAdminChangelistModelButtonMixin,
                         BaseModelAdmin):

    fields = ['subject_identifier', 'approximate_date', 'identity', 'first_name', 'last_name',
              'visit_code', 'dob']

    list_display = ['subject_identifier', 'identity', 'contacted', 'first_name', 'last_name',
                    'approximate_date', 'visit_code', 'dob']

    list_filter = ['subject_identifier', 'identity', 'contacted', 'approximate_date', 'visit_code']

    radio_fields = {
        'gender': admin.VERTICAL
    }

    search_fields = ['identity', 'subject_identifier', 'visit_code', 'first_name']

    readonly_fields = ['subject_identifier', 'identity', 'visit_code', 'first_name', 'last_name',
                       'initials', 'dob']

#     def consent_button(self, obj):
#         reverse_args = None
#         try:
#             subject_consent = MaternalConsent.objects.get(potential_subject=obj)
#             reverse_args = (subject_consent.pk, )
#         except MaternalConsent.DoesNotExist:
#             pass
#         return self.changelist_model_button(
#             'td_maternal', 'MaternalConsent', reverse_args=reverse_args,
#             change_label='consent')
#     consent_button.short_description = 'Consent'
