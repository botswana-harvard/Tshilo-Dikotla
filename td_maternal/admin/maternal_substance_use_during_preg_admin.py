from django.contrib import admin

from ..forms import MaternalSubstanceUseDuringPregForm
from ..models import MaternalSubstanceUseDuringPreg

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalSubstanceUseDuringPregAdmin(BaseMaternalModelAdmin):

    form = MaternalSubstanceUseDuringPregForm

    list_display = (
        'smoked_during_pregnancy',
        'smoking_during_preg_freq',
        'alcohol_during_pregnancy',
        'alcohol_during_preg_freq',
        'marijuana_during_preg',
        'marijuana_during_preg_freq',
    )

    radio_fields = {
        'smoked_during_pregnancy': admin.VERTICAL,
        'smoking_during_preg_freq': admin.VERTICAL,
        'alcohol_during_pregnancy': admin.VERTICAL,
        'alcohol_during_preg_freq': admin.VERTICAL,
        'marijuana_during_preg': admin.VERTICAL,
        'marijuana_during_preg_freq': admin.VERTICAL}

admin.site.register(
    MaternalSubstanceUseDuringPreg, MaternalSubstanceUseDuringPregAdmin)
