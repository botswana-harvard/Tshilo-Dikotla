from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_export.actions import export_as_csv_action

from ..forms import MaternalEligibilityForm
from ..models import MaternalEligibility


class MaternalEligibilityAdmin(BaseModelAdmin):

    form = MaternalEligibilityForm

    fields = ('eligibility_id',
              'report_datetime',
              'age_in_years',
              'has_omang',
              'currently_pregnant',
              'recently_delivered')
    radio_fields = {'currently_pregnant': admin.VERTICAL,
                    'recently_delivered': admin.VERTICAL,
                    'has_omang': admin.VERTICAL}

    readonly_fields = ('eligibility_id',)
    list_display = ('report_datetime', 'age_in_years', 'is_eligible',
                    'is_consented', 'currently_pregnant', 'recently_delivered')
    list_filter = ('report_datetime', 'is_eligible', 'is_consented',
                   'currently_pregnant', 'recently_delivered')

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

admin.site.register(MaternalEligibility, MaternalEligibilityAdmin)
