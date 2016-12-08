from django.contrib import admin

from ..admin_site import td_maternal_admin
from ..forms import MaternalDemographicsForm
from ..models import MaternalDemographics

from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(MaternalDemographics, site=td_maternal_admin)
class MaternalDemographicsAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalDemographicsForm
#     fields = ('maternal_visit',
#               'marital_status',
#               'marital_status_other',
#               'ethnicity',
#               'ethnicity_other',
#               'highest_education',
#               'current_occupation',
#               'current_occupation_other',
#               'provides_money',
#               'provides_money_other',
#               'money_earned',
#               'money_earned_other',
#               'own_phone',
#               'water_source',
#               'house_electrified',
#               'house_fridge',
#               'cooking_method',
#               'hh_goods',
#               'toilet_facility',
#               'toilet_facility_other',
#               'house_people_number',
#               'house_type')
    list_display = ('maternal_visit',
                    'marital_status',
                    'ethnicity',
                    'highest_education',
                    'own_phone')
    list_filter = ('marital_status',
                   'ethnicity',
                   'highest_education',
                   'own_phone')
    radio_fields = {'marital_status': admin.VERTICAL,
                    'ethnicity': admin.VERTICAL,
                    'highest_education': admin.VERTICAL,
                    'current_occupation': admin.VERTICAL,
                    'provides_money': admin.VERTICAL,
                    'money_earned': admin.VERTICAL,
                    'own_phone': admin.VERTICAL,
                    'water_source': admin.VERTICAL,
                    'house_electrified': admin.VERTICAL,
                    'house_fridge': admin.VERTICAL,
                    'cooking_method': admin.VERTICAL,
                    'toilet_facility': admin.VERTICAL,
                    'house_type': admin.VERTICAL}
#     filter_horizontal = ('hh_goods',)
