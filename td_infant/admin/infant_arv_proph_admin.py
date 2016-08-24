from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.mixins import TabularInlineMixin
from edc_export.actions import export_as_csv_action

from ..models import InfantArvProphMod, InfantArvProph
from ..forms import InfantArvProphForm, InfantArvProphModForm

from .admin_mixins import InfantScheduleModelModelAdminMixin


class InfantArvProphModInline(TabularInlineMixin, admin.TabularInline):

    model = InfantArvProphMod
    form = InfantArvProphModForm
    extra = 1


@admin.register(InfantArvProph)
class InfantArvProphAdmin(InfantScheduleModelModelAdminMixin, admin.ModelAdmin):

    form = InfantArvProphForm
    inlines = [InfantArvProphModInline, ]
    radio_fields = {
        'prophylatic_nvp': admin.VERTICAL,
        'arv_status': admin.VERTICAL,
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant NVP or AZT Proph",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'infant_visit__appointment__registered_subject__gender',
                 'dob': 'infant_visit__appointment__registered_subject__dob',
                 }),
        )]


@admin.register(InfantArvProphMod)
class InfantArvProphModAdmin(InfantScheduleModelModelAdminMixin, admin.ModelAdmin):

    form = InfantArvProphModForm

    list_filter = ('infant_arv_proph',)

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant NVP or AZT Proph",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'infant_arv_proph__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'infant_arv_proph__infant_visit__appointment__registered_subject__gender',
                 'dob': 'infant_arv_proph__infant_visit__appointment__registered_subject__dob',
                 'prophylatic_nvp': 'infant_arv_proph__prophylatic_nvp',
                 'arv_status': 'infant_arv_proph__arv_status',
                 }),
        )]
