from django.contrib import admin

from edc_consent.actions import flag_as_verified_against_paper, unflag_as_verified_against_paper

from td.admin_mixins import ModelAdminMixin

from ..forms import MaternalConsentForm
from ..models import MaternalConsent, MaternalEligibility
from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin
from django.urls.base import reverse


@admin.register(MaternalConsent)
class MaternalConsentAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    form = MaternalConsentForm

    fields = ('maternal_eligibility',
              'first_name',
              'last_name',
              'initials',
              'language',
              'study_site',
              'recruit_source',
              'recruit_source_other',
              'recruitment_clinic',
              'recruitment_clinic_other',
              'is_literate',
              'witness_name',
              'consent_datetime',
              'dob',
              'is_dob_estimated',
              'citizen',
              'identity',
              'identity_type',
              'confirm_identity',
              'comment',
              'consent_reviewed',
              'study_questions',
              'assessment_score',
              'consent_signature',
              'consent_copy')

    search_fields = ('subject_identifier', 'id', 'identity', 'first_name', 'last_name')

    radio_fields = {
        'assessment_score': admin.VERTICAL,
        'citizen': admin.VERTICAL,
        'consent_copy': admin.VERTICAL,
        'consent_reviewed': admin.VERTICAL,
        'consent_signature': admin.VERTICAL,
        'identity_type': admin.VERTICAL,
        'is_dob_estimated': admin.VERTICAL,
        'is_literate': admin.VERTICAL,
        'language': admin.VERTICAL,
        'recruit_source': admin.VERTICAL,
        'recruitment_clinic': admin.VERTICAL,
        'study_questions': admin.VERTICAL}

    list_display = ('subject_identifier',
                    'is_verified',
                    'is_verified_datetime',
                    'first_name',
                    'initials',
                    'gender',
                    'dob',
                    'consent_datetime',
                    'recruit_source',
                    'recruitment_clinic',
                    'created',
                    'modified',
                    'user_created',
                    'user_modified')
    list_filter = ('language',
                   'is_verified',
                   'is_literate',
                   'identity_type')

    def redirect_url(self, request, obj, post_url_continue=None):
        args = request.GET.dict()
        args.pop(self.querystring_name)
        redirect_url = super(ModelAdminNextUrlRedirectMixin, self).redirect_url(
            request, obj, post_url_continue)
        if request.GET.get(self.querystring_name):
            url_name = request.GET.get(self.querystring_name)
            return reverse(url_name)
        return redirect_url

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_eligibility":
            kwargs["queryset"] = MaternalEligibility.objects.filter(
                pk__exact=request.GET.get('pk'))
        return super(MaternalConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
