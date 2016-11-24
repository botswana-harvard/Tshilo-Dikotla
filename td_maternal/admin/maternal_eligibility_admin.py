from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from tshilo_dikotla.admin_mixins import ModelAdminMixin

from ..forms import MaternalEligibilityForm
from ..models import MaternalEligibility
from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin


@admin.register(MaternalEligibility)
class MaternalEligibilityAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    form = MaternalEligibilityForm

    fields = ('eligibility_id',
              'report_datetime',
              'age_in_years',
              'has_omang')

    radio_fields = {'has_omang': admin.VERTICAL}

    readonly_fields = ('eligibility_id',)

    list_display = ('report_datetime', 'age_in_years', 'is_eligible', 'is_consented')

    list_filter = ('report_datetime', 'is_eligible', 'is_consented')

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Eligibility",
            fields=[],
            delimiter=',',
            exclude=['user_created', 'user_modified', 'hostname_created', 'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'registered_subject__subject_identifier',
                 'gender': 'registered_subject__gender',
                 'dob': 'registered_subject__dob',
                 }),
        )]
