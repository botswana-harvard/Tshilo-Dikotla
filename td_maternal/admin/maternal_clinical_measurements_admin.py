from django.contrib import admin

from ..forms import MaternalClinicalMeasurementsOneForm, MaternalClinicalMeasurementsTwoForm
from ..models import MaternalClinicalMeasurementsOne, MaternalClinicalMeasurementsTwo

from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(MaternalClinicalMeasurementsOne)
class MaternalClinicalMeasurementsOneAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalClinicalMeasurementsOneForm

    list_display = ('weight_kg', 'height', 'systolic_bp', 'diastolic_bp')


@admin.register(MaternalClinicalMeasurementsTwo)
class MaternalClinicalMeasurementsTwoAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalClinicalMeasurementsTwoForm

    list_display = ('weight_kg', 'systolic_bp', 'diastolic_bp')
