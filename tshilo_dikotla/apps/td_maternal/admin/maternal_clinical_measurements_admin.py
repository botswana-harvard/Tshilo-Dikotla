from django.contrib import admin

from ..forms import MaternalClinicalMeasurementsOneForm, MaternalClinicalMeasurementsTwoForm
from ..models import MaternalClinicalMeasurementsOne, MaternalClinicalMeasurementsTwo

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalClinicalMeasurementsOneAdmin(BaseMaternalModelAdmin):

    form = MaternalClinicalMeasurementsOneForm

    list_display = ('weight_kg', 'height', 'systolic_bp', 'diastolic_bp')

admin.site.register(MaternalClinicalMeasurementsOne, MaternalClinicalMeasurementsOneAdmin)


class MaternalClinicalMeasurementsTwoAdmin(BaseMaternalModelAdmin):

    form = MaternalClinicalMeasurementsTwoForm

    list_display = ('weight_kg', 'systolic_bp', 'diastolic_bp')

admin.site.register(MaternalClinicalMeasurementsTwo, MaternalClinicalMeasurementsTwoAdmin)
