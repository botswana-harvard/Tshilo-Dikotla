from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action
from edc_base.modeladmin.admin import BaseTabularInline

from ..forms import MaternalArvPregForm, MaternalArvForm
from ..models import MaternalArvPreg, MaternalArv

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalArvInlineAdmin(BaseTabularInline):
    model = MaternalArv
    form = MaternalArvForm
    extra = 1


class MaternalArvAdmin(BaseMaternalModelAdmin):
    form = MaternalArvForm

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal ARV In This Preg: Pregnancy with list",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'maternal_arv_preg__maternal_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'maternal_arv_preg__maternal_visit__appointment__registered_subject__gender',
                 'dob': 'maternal_arv_preg__maternal_visit__appointment__registered_subject__dob',
                 'took_arv': 'maternal_arv_preg__took_arv',
                 'is_interrupt': 'maternal_arv_preg__is_interrupt',
                 'interrupt': 'maternal_arv_preg__interrupt',
                 'interrupt_other': 'maternal_arv_preg__interrupt_other'}),
        )]


class MaternalArvPregAdmin(BaseMaternalModelAdmin):
    form = MaternalArvPregForm
    inlines = [MaternalArvInlineAdmin, ]
    list_display = ('maternal_visit', 'took_arv',)
    list_filter = ('took_arv',)
    radio_fields = {'took_arv': admin.VERTICAL,
                    'is_interrupt': admin.VERTICAL,
                    'interrupt': admin.VERTICAL
                    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal ARV In This Preg: Pregnancy",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'maternal_arv_preg__maternal_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'maternal_arv_preg__maternal_visit__appointment__registered_subject__gender',
                 'dob': 'maternal_arv_preg__maternal_visit__appointment__registered_subject__dob',
                 }),
        )]

admin.site.register(MaternalArvPreg, MaternalArvPregAdmin)
