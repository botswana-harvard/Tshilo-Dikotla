from django.contrib import admin

from ..forms import NvpDispensingForm
from ..models import NvpDispensing, MaternalLabourDel

from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(NvpDispensing)
class NvpDispensingAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = NvpDispensingForm

    radio_fields = {'medication_instructions': admin.VERTICAL,
                    'correct_dose': admin.VERTICAL,
                    'dose_adjustment': admin.VERTICAL}

    list_display = ('report_datetime', 'medication_instructions', 'correct_dose',)

    list_filter = ('medication_instructions', 'correct_dose', 'dose_adjustment',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'maternal_delivery' and request.GET.get('subject_identifier'):
            kwargs["queryset"] = MaternalLabourDel.objects.filter(
                registered_subject__subject_identifier=request.GET.get('subject_identifier'))

        return super(NvpDispensingAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
