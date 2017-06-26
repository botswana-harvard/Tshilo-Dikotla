from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

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

    actions = [
        export_as_csv_action(
            description="CSV Export of Infant Congenital Anomalies",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'infant_visit__appointment__registered_subject__subject_identifier',
                 }),
        )]

admin.site.register(SolidFoodAssessment, SolidFoodAssessmentAdmin)
