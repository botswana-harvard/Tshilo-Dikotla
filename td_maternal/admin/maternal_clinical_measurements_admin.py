from django.contrib import admin

from ..admin_site import td_maternal_admin
from ..forms import MaternalClinicalMeasurementsOneForm, MaternalClinicalMeasurementsTwoForm
from ..models import MaternalClinicalMeasurementsOne, MaternalClinicalMeasurementsTwo

from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(MaternalClinicalMeasurementsOne, site=td_maternal_admin)
class MaternalClinicalMeasurementsOneAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalClinicalMeasurementsOneForm

    list_display = ('weight_kg', 'height', 'systolic_bp', 'diastolic_bp')


@admin.register(MaternalClinicalMeasurementsTwo, site=td_maternal_admin)
class MaternalClinicalMeasurementsTwoAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalClinicalMeasurementsTwoForm

    list_display = ('weight_kg', 'systolic_bp', 'diastolic_bp')
