from collections import OrderedDict
from django.core.urlresolvers import reverse

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from tshilo_dikotla.base_model_admin import BaseModelAdmin

from ..forms import MaternalEligibilityForm
from ..models import MaternalEligibility


class MaternalEligibilityAdmin(BaseModelAdmin):

    form = MaternalEligibilityForm

    fields = ('eligibility_id',
              'report_datetime',
              'age_in_years',
              'has_omang')

    search_fields = ['registered_subject__subject_identifier',
                     'registered_subject__initials']

    radio_fields = {'has_omang': admin.VERTICAL}

    readonly_fields = ('eligibility_id',)

    list_display = (
        'report_datetime', 'age_in_years', 'is_eligible', 'is_consented')

    list_filter = ('report_datetime', 'is_eligible', 'is_consented')

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Eligibility",
            fields=[],
            delimiter=',',
            exclude=['user_created', 'user_modified',
                     'hostname_created', 'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'registered_subject__subject_identifier',
                 'gender': 'registered_subject__gender',
                 'dob': 'registered_subject__dob',
                 }),
        )]

    def redirect_url(self, request, obj, post_url_continue=None):
        url_name = request.GET.get(self.querystring_name)
        section_name = request.GET.get('section_name')
        return reverse(url_name, kwargs={'section_name': section_name})


admin.site.register(MaternalEligibility, MaternalEligibilityAdmin)
