from django.contrib import admin

from tshilo_dikotla.base_model_admin import BaseModelAdmin
from ..forms import SolidFoodAssessementForm
from ..models import SolidFoodAssessment

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class SolidFoodAssessmentAdmin(BaseInfantScheduleModelAdmin, BaseModelAdmin):

    form = SolidFoodAssessementForm

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
    filter_horizontal = ('solid_foods', 'rations_receviced')

admin.site.register(SolidFoodAssessment, SolidFoodAssessmentAdmin)
