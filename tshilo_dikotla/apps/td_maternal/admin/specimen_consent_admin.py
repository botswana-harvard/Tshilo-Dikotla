from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action
from edc_consent.actions import flag_as_verified_against_paper, unflag_as_verified_against_paper
from edc_registration.models import RegisteredSubject

from tshilo_dikotla.apps.td.base_model_admin import BaseModelAdmin

from ..forms import SpecimenConsentForm
from ..models import SpecimenConsent


class SpecimenConsentAdmin(BaseModelAdmin):

    dashboard_type = 'maternal'
    form = SpecimenConsentForm

    fields = ('registered_subject',
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
                    'registered_subject',
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
    actions = [
        flag_as_verified_against_paper,
        unflag_as_verified_against_paper,
        export_as_csv_action(
            description="CSV Export of Specimen Consent",
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
        return super(SpecimenConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SpecimenConsent, SpecimenConsentAdmin)
