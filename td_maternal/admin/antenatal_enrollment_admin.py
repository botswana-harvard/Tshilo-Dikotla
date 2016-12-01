from django.contrib import admin

from td.admin_mixins import ModelAdminMixin

from ..forms import AntenatalEnrollmentForm
from ..models import AntenatalEnrollment
from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin


@admin.register(AntenatalEnrollment)
class AntenatalEnrollmentAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    dashboard_type = 'maternal'
    form = AntenatalEnrollmentForm

    fields = ('subject_identifier',
              'report_datetime',
              'knows_lmp',
              'last_period_date',
              'edd_by_lmp',
              'ga_lmp_enrollment_wks',
              'ga_lmp_anc_wks',
              'is_diabetic',
              'will_breastfeed',
              'will_remain_onstudy',
              'current_hiv_status',
              'evidence_hiv_status',
              'week32_test',
              'week32_test_date',
              'week32_result',
              'evidence_32wk_hiv_status',
              'will_get_arvs',
              'rapid_test_done',
              'rapid_test_date',
              'rapid_test_result',
              'enrollment_hiv_status')
    readonly_fields = ('subject_identifier', 'edd_by_lmp', 'ga_lmp_enrollment_wks', 'enrollment_hiv_status')
    radio_fields = {'is_diabetic': admin.VERTICAL,
                    'will_breastfeed': admin.VERTICAL,
                    'will_remain_onstudy': admin.VERTICAL,
                    'current_hiv_status': admin.VERTICAL,
                    'week32_test': admin.VERTICAL,
                    'week32_result': admin.VERTICAL,
                    'evidence_32wk_hiv_status': admin.VERTICAL,
                    'evidence_hiv_status': admin.VERTICAL,
                    'will_get_arvs': admin.VERTICAL,
                    'rapid_test_done': admin.VERTICAL,
                    'rapid_test_result': admin.VERTICAL,
                    'knows_lmp': admin.VERTICAL}
    list_display = ('report_datetime', 'evidence_hiv_status',
                    'will_get_arvs', 'ga_lmp_anc_wks', 'enrollment_hiv_status')
