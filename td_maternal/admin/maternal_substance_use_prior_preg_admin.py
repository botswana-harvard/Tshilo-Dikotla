from django.contrib import admin

from ..forms import MaternalSubstanceUsePriorPregForm
from ..models import MaternalSubstanceUsePriorPreg

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalSubstanceUsePriorPregAdmin(BaseMaternalModelAdmin):

    form = MaternalSubstanceUsePriorPregForm

    list_display = (
        'smoked_prior_to_preg',
        'smoking_prior_preg_freq',
        'alcohol_prior_pregnancy',
        'alcohol_prior_preg_freq',
        'marijuana_prior_preg',
        'marijuana_prior_preg_freq',
    )

    radio_fields = {
        'smoked_prior_to_preg': admin.VERTICAL,
        'smoking_prior_preg_freq': admin.VERTICAL,
        'alcohol_prior_pregnancy': admin.VERTICAL,
        'alcohol_prior_preg_freq': admin.VERTICAL,
        'marijuana_prior_preg': admin.VERTICAL,
        'marijuana_prior_preg_freq': admin.VERTICAL
    }

admin.site.register(MaternalSubstanceUsePriorPreg, MaternalSubstanceUsePriorPregAdmin)
