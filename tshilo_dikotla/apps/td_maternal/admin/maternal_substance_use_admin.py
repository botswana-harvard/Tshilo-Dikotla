from django.contrib import admin

from ..forms import MaternalSubstanceUseForm, MaternalSubstanceUseTwoForm
from ..models import MaternalSubstanceUse, MaternalSubstanceUseTwo

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalSubstanceUseAdmin(BaseMaternalModelAdmin):

    form = MaternalSubstanceUseForm

    list_display = (
        'smoked_prior_to_preg', 'smoking_prior_preg_freq',
        'smoked_during_pregnancy', 'smoking_during_preg_freq', 'alcohol_during_pregnancy'
        'alcohol_during_preg_freq', 'marijuana_prior_preg', 'marijuana_prior_preg_freq',
        'marijuana_during_preg', 'marijuana_during_preg_freq',)
    
    radio_fields = {
        'smoked_prior_to_preg': admin.VERTICAL, 'smoking_prior_preg_freq': admin.VERTICAL,
        'smoked_during_pregnancy': admin.VERTICAL, 'smoking_during_preg_freq': admin.VERTICAL,
        'alcohol_during_pregnancy': admin.VERTICAL, 'alcohol_during_preg_freq': admin.VERTICAL,
        'marijuana_prior_preg': admin.VERTICAL, 'marijuana_prior_preg_freq': admin.VERTICAL,
        'marijuana_during_preg': admin.VERTICAL, 'marijuana_during_preg_freq': admin.VERTICAL}

admin.site.register(MaternalSubstanceUse, MaternalSubstanceUseAdmin)


class MaternalSubstanceUseTwoAdmin(BaseMaternalModelAdmin):

    form = MaternalSubstanceUseTwoForm

    list_display = (
        'smoked_prior_to_preg', 'smoked_prior_to_preg', 'smoking_prior_preg_freq',
        'smoked_during_pregnancy', 'smoking_during_preg_freq', 'alcohol_during_pregnancy'
        'alcohol_during_preg_freq', 'marijuana_prior_preg', 'marijuana_prior_preg_freq',
        'marijuana_during_preg', 'marijuana_during_preg_freq',)

    radio_fields = {
        'smoked_prior_to_preg': admin.VERTICAL, 'smoking_prior_preg_freq': admin.VERTICAL,
        'smoked_during_pregnancy': admin.VERTICAL, 'smoking_during_preg_freq': admin.VERTICAL,
        'alcohol_during_pregnancy': admin.VERTICAL, 'alcohol_during_preg_freq': admin.VERTICAL,
        'marijuana_prior_preg': admin.VERTICAL, 'marijuana_prior_preg_freq': admin.VERTICAL,
        'marijuana_during_preg': admin.VERTICAL, 'marijuana_during_preg_freq': admin.VERTICAL}

admin.site.register(MaternalSubstanceUseTwo, MaternalSubstanceUseTwoAdmin)