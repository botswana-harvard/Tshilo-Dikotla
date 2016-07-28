from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from tshilo_dikotla.base_model_admin import BaseModelAdmin
from ..forms import SolidFoodAssessementForm
from ..models import SolidFoodAssessment

class SolidFoodAssessmentAdmin(BaseModelAdmin):
    
    form = SolidFoodAssessementForm

    list_display = ()
    list_filter = ('rations_receviced', 'solid_foods')
    radio_fields = {'porridge': admin.VERTICAL,
                    'tsabana': admin.VERTICAL,
                    'mother_tsabana': admin.VERTICAL,
                    'meat': admin.VERTICAL,
                    'potatoes': admin.VERTICAL,
                    'carrot_swt_potato': admin.VERTICAL,
                    'green_veg': admin.VERTICAL,
                    'fresh_fruits': admin.VERTICAL,
                    'fullcream_milk': admin.VERTICAL,
                    'skim_milk': admin.VERTICAL,
                    'raw_milk': admin.VERTICAL,
                    'juice': admin.VERTICAL,
                    'eggs': admin.VERTICAL,
                    'yogurt': admin.VERTICAL,
                    'cheese': admin.VERTICAL,
                    'rations': admin.VERTICAL,
                     
                    }
    filter_horizontal = ()

admin.site.register(SolidFoodAssessment, SolidFoodAssessmentAdmin)
