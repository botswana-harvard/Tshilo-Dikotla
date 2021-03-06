from django.contrib import admin
from collections import OrderedDict

from edc_registration.models import RegisteredSubject
from edc_export.actions import export_as_csv_action

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin

from ..forms import AntenatalEnrollmentForm
from ..models import AntenatalEnrollment


class AntenatalEnrollmentAdmin(MembershipBaseModelAdmin):

    dashboard_type = 'maternal'
    form = AntenatalEnrollmentForm

    search_fields = ['registered_subject__subject_identifier',
                     'registered_subject__initials']

    fields = ('registered_subject',
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
    readonly_fields = (
        'edd_by_lmp', 'ga_lmp_enrollment_wks', 'enrollment_hiv_status')
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
    list_display = ('registered_subject', 'report_datetime', 'evidence_hiv_status',
                    'will_get_arvs', 'ga_lmp_anc_wks', 'enrollment_hiv_status')

    actions = [
        export_as_csv_action(
            description="CSV Export of Antenatal Enrollment",
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
        return super(AntenatalEnrollmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(AntenatalEnrollment, AntenatalEnrollmentAdmin)
