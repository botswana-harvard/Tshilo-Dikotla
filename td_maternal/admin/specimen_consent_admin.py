from django.contrib import admin

from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin

from td.admin_mixins import ModelAdminMixin

from ..admin_site import td_maternal_admin
from ..forms import SpecimenConsentForm
from ..models import SpecimenConsent


@admin.register(SpecimenConsent, site=td_maternal_admin)
class SpecimenConsentAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    dashboard_type = 'maternal'
    form = SpecimenConsentForm

    fields = ('subject_identifier',
              'consent_datetime',
              'language',
              'may_store_samples',
              'is_literate',
              'witness_name',
              'purpose_explained',
              'purpose_understood',
              'offered_copy')
    radio_fields = {'language': admin.VERTICAL,
                    'may_store_samples': admin.VERTICAL,
                    'is_literate': admin.VERTICAL,
                    'purpose_explained': admin.VERTICAL,
                    'purpose_understood': admin.VERTICAL,
                    'offered_copy': admin.VERTICAL, }

    list_display = ('subject_identifier',
                    'is_verified',
                    'is_verified_datetime',
                    'consent_datetime',
                    'created',
                    'modified',
                    'user_created',
                    'user_modified')
    list_filter = ('language',
                   'is_verified',
                   'is_literate')
    actions = []
