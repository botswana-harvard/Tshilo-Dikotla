from django.contrib import admin

from ..admin_site import td_maternal_admin
from ..forms import MaternalDiagnosesForm
from ..models import MaternalDiagnoses

from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(MaternalDiagnoses, site=td_maternal_admin)
class MaternalDiagnosesAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalDiagnosesForm
    list_display = ('maternal_visit', 'new_diagnoses', 'has_who_dx')
    list_filter = ('new_diagnoses', 'has_who_dx')
    radio_fields = {'new_diagnoses': admin.VERTICAL,
                    'has_who_dx': admin.VERTICAL}
    filter_horizontal = ('who', 'diagnoses')
