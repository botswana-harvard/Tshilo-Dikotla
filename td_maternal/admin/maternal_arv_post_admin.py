from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action
from edc_base.modeladmin.admin import BaseTabularInline

from ..forms import MaternalArvPostForm, MaternalArvPostMedForm, MaternalArvPostAdhForm
from ..models import MaternalVisit, MaternalArvPost, MaternalArvPostMed, MaternalArvPostAdh

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalArvPostModInlineAdmin(BaseTabularInline):

    model = MaternalArvPostMed
    form = MaternalArvPostMedForm
    extra = 1


class MaternalArvPostModAdmin(BaseMaternalModelAdmin):

    form = MaternalArvPostMedForm
    list_display = ('maternal_arv_post', 'arv_code',
                    'dose_status', 'modification_date', 'modification_code')

    search_fields = [
        'maternal_arv_post__maternal_visit__appointment__registered_subject__subject_identifier',
        'maternal_arv_post__maternal_visit__appointment__registered_subject__initials', ]

    radio_fields = {
        "arv_code": admin.VERTICAL,
        "dose_status": admin.VERTICAL,
        "modification_code": admin.VERTICAL,
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal ARV Post with list",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'maternal_arv_post__maternal_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'maternal_arv_post__maternal_visit__appointment__registered_subject__gender',
                 'dob': 'maternal_arv_post__maternal_visit__appointment__registered_subject__dob',
                 'on_arv_since': 'maternal_arv_post__on_arv_since',
                 'on_arv_reason': 'maternal_arv_post__on_arv_reason',
                 'on_arv_reason_other': 'maternal_arv_post__on_arv_reason_other',
                 'arv_status': 'maternal_arv_post__arv_status',
                 'visit_code': 'maternal_arv_post__maternal_visit__appointment__visit_definition__code',
                 'visit_reason': 'maternal_arv_post__maternal_visit__reason',
                 'visit_study_status': 'maternal_arv_post__maternal_visit__study_status',
                 }),
        )]

admin.site.register(MaternalArvPostMed, MaternalArvPostModAdmin)


class MaternalArvPostAdmin(BaseMaternalModelAdmin):

    form = MaternalArvPostForm

    fields = (
        "maternal_visit",
        "on_arv_since",
        "on_arv_reason",
        "on_arv_reason_other",
        "arv_status")

    radio_fields = {
        "on_arv_since": admin.VERTICAL,
        "on_arv_reason": admin.VERTICAL,
        "arv_status": admin.VERTICAL}
    inlines = [MaternalArvPostModInlineAdmin, ]

admin.site.register(MaternalArvPost, MaternalArvPostAdmin)


class MaternalArvPostAdhAdmin(BaseMaternalModelAdmin):

    form = MaternalArvPostAdhForm
    fields = (
        "maternal_visit",
        "missed_doses",
        "missed_days",
        "missed_days_discnt",
        "comment")

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal ARVs Post: Adherence",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'maternal_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'maternal_visit__appointment__registered_subject__gender',
                 'dob': 'maternal_visit__appointment__registered_subject__dob',
                 'registered': 'maternal_visit__appointment__registered_subject__registration_datetime'}),
        )]

admin.site.register(MaternalArvPostAdh, MaternalArvPostAdhAdmin)
