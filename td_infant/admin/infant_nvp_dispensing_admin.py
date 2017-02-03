from django.contrib import admin

from ..forms import InfantNvpDispensingForm
from ..models import InfantNvpDispensing, MaternalLabDel

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantNvpDispensingAdmin(BaseInfantScheduleModelAdmin, admin.ModelAdmin):

    form = InfantNvpDispensingForm

    radio_fields = {'nvp_prophylaxis': admin.VERTICAL,
                    'azt_prophylaxis': admin.VERTICAL,
                    'medication_instructions': admin.VERTICAL,
                    'correct_dose': admin.VERTICAL}

    list_display = ('infant_visit', 'nvp_prophylaxis', 'azt_prophylaxis', 'medication_instructions',)

    list_filter = ('nvp_prophylaxis', 'azt_prophylaxis', 'correct_dose',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'maternal_delivery' and request.GET.get('subject_identifier'):
            kwargs["queryset"] = MaternalLabDel.objects.filter(
                subject_identifier=request.GET.get('subject_identifier'))

        return super(InfantNvpDispensingAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(InfantNvpDispensing, InfantNvpDispensingAdmin)
