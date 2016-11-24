from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin_mixins import TabularInlineMixin
from edc_export.actions import export_as_csv_action

from tshilo_dikotla.constants import INFANT

from ..models import (
    InfantCongenitalAnomalies, InfantCns, InfantFacialDefect,
    InfantCleftDisorder, InfantMouthUpGi, InfantCardioDisorder,
    InfantRespiratoryDefect, InfantLowerGi, InfantMaleGenital,
    InfantFemaleGenital, InfantRenal, InfantMusculoskeletal,
    InfantSkin, InfantTrisomies)
from ..forms import (
    InfantCongenitalAnomaliesForm, InfantFacialDefectForm,
    InfantCleftDisorderForm, InfantMouthUpGiForm,
    InfantCardioDisorderForm,
    InfantRespiratoryDefectForm, InfantLowerGiForm,
    InfantFemaleGenitalForm,
    InfantMaleGenitalForm, InfantRenalForm,
    InfantMusculoskeletalForm,
    InfantSkinForm, InfantTrisomiesForm,
    InfantCnsForm)

from .admin_mixins import CrfModelAdminMixin


@admin.register(InfantCns)
class InfantCnsAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = InfantCnsForm
    list_display = ('congenital_anomalies', 'abnormality_status',)

    list_filter = ('cns',)

    radio_fields = {
        'cns': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }
    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Central Nervous System abnormality",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'congenital_anomalies__infant_visit__appointment__registered_subject__gender',
                 'dob': 'congenital_anomalies__infant_visit__appointment__registered_subject__dob',
                 }),
        )]


class InfantCnsInline(TabularInlineMixin, admin.TabularInline):

    model = InfantCns
    form = InfantCnsForm
    extra = 0


@admin.register(InfantFacialDefect)
class InfantFacialDefectAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = InfantFacialDefectForm
    list_display = ('congenital_anomalies',)

    radio_fields = {
        'facial_defect': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Facial Defect abnormality",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'congenital_anomalies__infant_visit__appointment__registered_subject__gender',
                 'dob': 'congenital_anomalies__infant_visit__appointment__registered_subject__dob',
                 }),
        )]


class InfantFacialDefectInline(TabularInlineMixin, admin.TabularInline):

    model = InfantFacialDefect
    form = InfantFacialDefectForm
    extra = 0


@admin.register(InfantCleftDisorder)
class InfantCleftDisorderAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = InfantCleftDisorderForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'cleft_disorder': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Cleft Disorder abnormality",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'congenital_anomalies__infant_visit__appointment__registered_subject__gender',
                 'dob': 'congenital_anomalies__infant_visit__appointment__registered_subject__dob',
                 }),
        )]


class InfantCleftDisorderInline(TabularInlineMixin, admin.TabularInline):

    model = InfantCleftDisorder
    form = InfantCleftDisorderForm
    extra = 0


class InfantMouthUpGiAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = InfantMouthUpGiForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'mouth_up_gi': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Mouth Up Gastrointestinal abnormality",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'congenital_anomalies__infant_visit__appointment__registered_subject__gender',
                 'dob': 'congenital_anomalies__infant_visit__appointment__registered_subject__dob',
                 }),
        )]

admin.site.register(InfantMouthUpGi, InfantMouthUpGiAdmin)


class InfantMouthUpGiInline(TabularInlineMixin, admin.TabularInline):

    model = InfantMouthUpGi
    form = InfantMouthUpGiForm
    extra = 0


@admin.register(InfantCardioDisorder)
class InfantCardioDisorderAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = InfantCardioDisorderForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'cardio_disorder': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Cardiovascular Disorder abnormality",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'congenital_anomalies__infant_visit__appointment__registered_subject__gender',
                 'dob': 'congenital_anomalies__infant_visit__appointment__registered_subject__dob',
                 }),
        )]


class InfantCardioDisorderInline(TabularInlineMixin, admin.TabularInline):

    model = InfantCardioDisorder
    form = InfantCardioDisorderForm
    extra = 0


@admin.register(InfantRespiratoryDefect)
class InfantRespiratoryDefectAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = InfantRespiratoryDefectForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'respiratory_defect': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Respiratory Defect abnormality",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'congenital_anomalies__infant_visit__appointment__registered_subject__gender',
                 'dob': 'congenital_anomalies__infant_visit__appointment__registered_subject__dob',
                 }),
        )]


class InfantRespiratoryDefectInline(TabularInlineMixin, admin.TabularInline):

    model = InfantRespiratoryDefect
    form = InfantRespiratoryDefectForm
    extra = 0


@admin.register(InfantLowerGi)
class InfantLowerGiAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = InfantLowerGiForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'lower_gi': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Lower Gastrointestinal abnormality",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'congenital_anomalies__infant_visit__appointment__registered_subject__gender',
                 'dob': 'congenital_anomalies__infant_visit__appointment__registered_subject__dob',
                 }),
        )]


class InfantLowerGiInline(TabularInlineMixin, admin.TabularInline):

    model = InfantLowerGi
    form = InfantLowerGiForm
    extra = 0


@admin.register(InfantFemaleGenital)
class InfantFemaleGenitalAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = InfantFemaleGenitalForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'female_genital': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Female Genital abnormality",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'congenital_anomalies__infant_visit__appointment__registered_subject__gender',
                 'dob': 'congenital_anomalies__infant_visit__appointment__registered_subject__dob',
                 }),
        )]


class InfantFemaleGenitalInline(TabularInlineMixin, admin.TabularInline):

    model = InfantFemaleGenital
    form = InfantFemaleGenitalForm
    extra = 0


@admin.register(InfantMaleGenital)
class InfantMaleGenitalAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = InfantMaleGenitalForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'male_genital': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Male Genital abnormality",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'congenital_anomalies__infant_visit__appointment__registered_subject__gender',
                 'dob': 'congenital_anomalies__infant_visit__appointment__registered_subject__dob',
                 }),
        )]


class InfantMaleGenitalInline(TabularInlineMixin, admin.TabularInline):

    model = InfantMaleGenital
    form = InfantMaleGenitalForm
    extra = 0


@admin.register(InfantRenal)
class InfantRenalAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = form = InfantRenalForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'renal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Renal abnormality",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'congenital_anomalies__infant_visit__appointment__registered_subject__gender',
                 'dob': 'congenital_anomalies__infant_visit__appointment__registered_subject__dob',
                 }),
        )]


class InfantRenalInline(TabularInlineMixin, admin.TabularInline):

    model = InfantRenal
    form = InfantRenalForm
    extra = 0


@admin.register(InfantMusculoskeletal)
class InfantMusculoskeletalAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = form = InfantMusculoskeletalForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'musculo_skeletal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Musculoskeletal abnormality",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'congenital_anomalies__infant_visit__appointment__registered_subject__gender',
                 'dob': 'congenital_anomalies__infant_visit__appointment__registered_subject__dob',
                 }),
        )]


class InfantMusculoskeletalInline(TabularInlineMixin, admin.TabularInline):

    model = InfantMusculoskeletal
    form = InfantMusculoskeletalForm
    extra = 0


@admin.register(InfantSkin)
class InfantSkinAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = form = InfantSkinForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'skin': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant skin abnormality",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'congenital_anomalies__infant_visit__appointment__registered_subject__gender',
                 'dob': 'congenital_anomalies__infant_visit__appointment__registered_subject__dob',
                 }),
        )]


class InfantSkinInline(TabularInlineMixin, admin.TabularInline):

    model = InfantSkin
    form = InfantSkinForm
    extra = 0


@admin.register(InfantTrisomies)
class InfantTrisomiesAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = InfantTrisomiesForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'trisomies': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant trisomies abnormality",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'congenital_anomalies__infant_visit__appointment__registered_subject__gender',
                 'dob': 'congenital_anomalies__infant_visit__appointment__registered_subject__dob',
                 }),
        )]


class InfantTrisomiesInline(TabularInlineMixin, admin.TabularInline):

    model = InfantTrisomies
    form = InfantTrisomiesForm
    extra = 0


@admin.register(InfantCongenitalAnomalies)
class InfantCongenitalAnomaliesAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = InfantCongenitalAnomaliesForm
    dashboard_type = INFANT
    visit_model_name = 'infantvisit'

    list_display = ('infant_visit',)

    inlines = [
        InfantCnsInline,
        InfantFacialDefectInline,
        InfantCleftDisorderInline,
        InfantMouthUpGiInline,
        InfantCardioDisorderInline,
        InfantRespiratoryDefectInline,
        InfantLowerGiInline,
        InfantFemaleGenitalInline,
        InfantMaleGenitalInline,
        InfantRenalInline,
        InfantMusculoskeletalInline,
        InfantSkinInline,
        InfantTrisomiesInline]
