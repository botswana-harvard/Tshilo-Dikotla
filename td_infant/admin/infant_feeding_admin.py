from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..forms import InfantFeedingForm
from ..models import InfantFeeding, InfantVisit

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantFeedingAdmin(BaseInfantScheduleModelAdmin):

    form = InfantFeedingForm
    fields = (
        "infant_visit",
        "report_datetime",
        "last_att_sche_visit",
        "other_feeding",
        "formula_intro_occur",
        "formula_intro_date",
        "took_formula",
        "is_first_formula",
        "date_first_formula",
        "est_date_first_formula",
        "water",
        "juice",
        "cow_milk",
        "cow_milk_yes",
        "other_milk",
        "other_milk_animal",
        "milk_boiled",
        "fruits_veg",
        "cereal_porridge",
        "solid_liquid",
        "rehydration_salts",
        "water_used",
        "water_used_other",
        "ever_breastfeed",
        "complete_weaning",
        "weaned_completely",
        "most_recent_bm",
        "times_breastfed",
        "comments")
    readonly_fields = ('last_att_sche_visit',)
    radio_fields = {
        "other_feeding": admin.VERTICAL,
        "formula_intro_occur": admin.VERTICAL,
        "water_used": admin.VERTICAL,
        "took_formula": admin.VERTICAL,
        "is_first_formula": admin.VERTICAL,
        "est_date_first_formula": admin.VERTICAL,
        "water": admin.VERTICAL,
        "juice": admin.VERTICAL,
        "cow_milk": admin.VERTICAL,
        "cow_milk_yes": admin.VERTICAL,
        "other_milk": admin.VERTICAL,
        "milk_boiled": admin.VERTICAL,
        "fruits_veg": admin.VERTICAL,
        "cereal_porridge": admin.VERTICAL,
        "solid_liquid": admin.VERTICAL,
        "rehydration_salts": admin.VERTICAL,
        "ever_breastfeed": admin.VERTICAL,
        "complete_weaning": admin.VERTICAL,
        "weaned_completely": admin.VERTICAL,
        "times_breastfed": admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Feeding",
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(InfantFeedingAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantFeeding, InfantFeedingAdmin)
