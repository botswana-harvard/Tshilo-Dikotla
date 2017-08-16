from django.contrib import admin

from ..models import InfantBirthArv

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantBirthArvAdmin(BaseInfantScheduleModelAdmin):

    list_display = (
        'infant_visit', 'azt_after_birth',
        'azt_dose_date', 'azt_additional_dose',
        'sdnvp_after_birth',)

    list_filter = ('azt_after_birth', 'azt_dose_date',
                   'azt_additional_dose', 'sdnvp_after_birth',)

    radio_fields = {
        'azt_after_birth': admin.VERTICAL,
        'azt_additional_dose': admin.VERTICAL,
        'sdnvp_after_birth': admin.VERTICAL,
        'azt_discharge_supply': admin.VERTICAL,
    }

admin.site.register(InfantBirthArv, InfantBirthArvAdmin)
