from django.contrib import admin

from ..forms import MaternalDiagnosesForm
from ..models import MaternalDiagnoses
from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalDiagnosesAdmin(BaseMaternalModelAdmin):

    form = MaternalDiagnosesForm
    list_display = ('maternal_visit', 'new_diagnoses', 'has_who_dx')
    list_filter = ('new_diagnoses', 'has_who_dx')
    radio_fields = {'new_diagnoses': admin.VERTICAL,
                    'has_who_dx': admin.VERTICAL}
    filter_horizontal = ('who', 'diagnoses')

admin.site.register(MaternalDiagnoses, MaternalDiagnosesAdmin)
