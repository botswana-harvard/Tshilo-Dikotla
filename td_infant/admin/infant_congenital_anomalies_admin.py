from collections import OrderedDict

from django.contrib import admin

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin
from edc_base.modeladmin.admin import BaseTabularInline
from edc_export.actions import export_as_csv_action
from tshilo_dikotla.constants import INFANT

from ..models import (
    InfantCongenitalAnomalies, InfantCns, InfantFacialDefect,
    InfantCleftDisorder, InfantMouthUpGi, InfantCardioDisorder,
    InfantRespiratoryDefect, InfantLowerGi, InfantMaleGenital,
    InfantFemaleGenital, InfantRenal, InfantMusculoskeletal,
    InfantSkin, InfantTrisomies
)


from ..forms import (
    InfantCongenitalAnomaliesForm, InfantFacialDefectForm,
    InfantCleftDisorderForm, InfantMouthUpGiForm,
    InfantCardioDisorderForm,
    InfantRespiratoryDefectForm, InfantLowerGiForm,
    InfantFemaleGenitalForm,
    InfantMaleGenitalForm, InfantRenalForm,
    InfantMusculoskeletalForm,
    InfantSkinForm, InfantTrisomiesForm,
    InfantCnsForm
)


class InfantCnsAdmin(BaseInfantScheduleModelAdmin):
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

admin.site.register(InfantCns, InfantCnsAdmin)


class InfantCnsInline(BaseTabularInline):

    model = InfantCns
    form = InfantCnsForm
    extra = 0


class InfantFacialDefectAdmin(BaseInfantScheduleModelAdmin):
    form = InfantFacialDefectForm
    list_display = ('congenital_anomalies',)

    radio_fields = {
        'facial_defect': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

    search_fields = [
        'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
        'congenital_anomalies__infant_visit__appointment__registered_subject__initials', ]

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
admin.site.register(InfantFacialDefect, InfantFacialDefectAdmin)


class InfantFacialDefectInline(BaseTabularInline):

    model = InfantFacialDefect
    form = InfantFacialDefectForm
    extra = 0


class InfantCleftDisorderAdmin(BaseInfantScheduleModelAdmin):
    form = InfantCleftDisorderForm

    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
        'congenital_anomalies__infant_visit__appointment__registered_subject__initials', ]

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

admin.site.register(InfantCleftDisorder, InfantCleftDisorderAdmin)


class InfantCleftDisorderInline(BaseTabularInline):

    model = InfantCleftDisorder
    form = InfantCleftDisorderForm
    extra = 0


class InfantMouthUpGiAdmin(BaseInfantScheduleModelAdmin):
    form = InfantMouthUpGiForm

    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
        'congenital_anomalies__infant_visit__appointment__registered_subject__initials', ]

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


class InfantMouthUpGiInline(BaseTabularInline):

    model = InfantMouthUpGi
    form = InfantMouthUpGiForm
    extra = 0


class InfantCardioDisorderAdmin(BaseInfantScheduleModelAdmin):
    form = InfantCardioDisorderForm

    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
        'congenital_anomalies__infant_visit__appointment__registered_subject__initials', ]

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

admin.site.register(InfantCardioDisorder, InfantCardioDisorderAdmin)


class InfantCardioDisorderInline(BaseTabularInline):

    model = InfantCardioDisorder
    form = InfantCardioDisorderForm
    extra = 0


class InfantRespiratoryDefectAdmin(BaseInfantScheduleModelAdmin):
    form = InfantRespiratoryDefectForm

    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
        'congenital_anomalies__infant_visit__appointment__registered_subject__initials', ]

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

admin.site.register(InfantRespiratoryDefect, InfantRespiratoryDefectAdmin)


class InfantRespiratoryDefectInline(BaseTabularInline):

    model = InfantRespiratoryDefect
    form = InfantRespiratoryDefectForm
    extra = 0


class InfantLowerGiAdmin(BaseInfantScheduleModelAdmin):
    form = InfantLowerGiForm

    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
        'congenital_anomalies__infant_visit__appointment__registered_subject__initials', ]

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

admin.site.register(InfantLowerGi, InfantLowerGiAdmin)


class InfantLowerGiInline(BaseTabularInline):

    model = InfantLowerGi
    form = InfantLowerGiForm
    extra = 0


class InfantFemaleGenitalAdmin(BaseInfantScheduleModelAdmin):
    form = InfantFemaleGenitalForm

    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
        'congenital_anomalies__infant_visit__appointment__registered_subject__initials', ]

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

admin.site.register(InfantFemaleGenital, InfantFemaleGenitalAdmin)


class InfantFemaleGenitalInline(BaseTabularInline):

    model = InfantFemaleGenital
    form = InfantFemaleGenitalForm
    extra = 0


class InfantMaleGenitalAdmin(BaseInfantScheduleModelAdmin):
    form = InfantMaleGenitalForm

    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
        'congenital_anomalies__infant_visit__appointment__registered_subject__initials', ]

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

admin.site.register(InfantMaleGenital, InfantMaleGenitalAdmin)


class InfantMaleGenitalInline(BaseTabularInline):

    model = InfantMaleGenital
    form = InfantMaleGenitalForm
    extra = 0


class InfantRenalAdmin(BaseInfantScheduleModelAdmin):
    form = form = InfantRenalForm

    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
        'congenital_anomalies__infant_visit__appointment__registered_subject__initials', ]

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

admin.site.register(InfantRenal, InfantRenalAdmin)


class InfantRenalInline(BaseTabularInline):

    model = InfantRenal
    form = InfantRenalForm
    extra = 0


class InfantMusculoskeletalAdmin(BaseInfantScheduleModelAdmin):
    form = form = InfantMusculoskeletalForm

    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
        'congenital_anomalies__infant_visit__appointment__registered_subject__initials', ]

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

admin.site.register(InfantMusculoskeletal, InfantMusculoskeletalAdmin)


class InfantMusculoskeletalInline(BaseTabularInline):

    model = InfantMusculoskeletal
    form = InfantMusculoskeletalForm
    extra = 0


class InfantSkinAdmin(BaseInfantScheduleModelAdmin):
    form = form = InfantSkinForm

    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
        'congenital_anomalies__infant_visit__appointment__registered_subject__initials', ]

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

admin.site.register(InfantSkin, InfantSkinAdmin)


class InfantSkinInline(BaseTabularInline):

    model = InfantSkin
    form = InfantSkinForm
    extra = 0


class InfantTrisomiesAdmin(BaseInfantScheduleModelAdmin):
    form = InfantTrisomiesForm

    list_display = ('congenital_anomalies',)

    search_fields = [
        'congenital_anomalies__infant_visit__appointment__registered_subject__subject_identifier',
        'congenital_anomalies__infant_visit__appointment__registered_subject__initials', ]

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

admin.site.register(InfantTrisomies, InfantTrisomiesAdmin)


class InfantTrisomiesInline(BaseTabularInline):

    model = InfantTrisomies
    form = InfantTrisomiesForm
    extra = 0


class InfantCongenitalAnomaliesAdmin(BaseInfantScheduleModelAdmin):

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

admin.site.register(InfantCongenitalAnomalies, InfantCongenitalAnomaliesAdmin)
