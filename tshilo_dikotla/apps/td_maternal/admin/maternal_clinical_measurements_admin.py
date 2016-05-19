from django.contrib import admin

from ..forms import MaternalClinicalMeasurementsOneForm
from ..models import MaternalClinicalMeasurementsOne

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalClinicalMeasurementsOneAdmin(BaseMaternalModelAdmin):

    form = MaternalClinicalMeasurementsOneForm

#     fields = ('maternal_visit',
#               'weight_kg',
#               'height',
#               'systolic_bp',
#               'diastolic_bp')
    list_display = ('weight_kg', 'height', 'systolic_bp', 'diastolic_bp')

admin.site.register(MaternalClinicalMeasurementsOne, MaternalClinicalMeasurementsOneAdmin)
