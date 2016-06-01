from django.contrib import admin

from ..forms import MaternalPostPartumFuForm
from ..models import MaternalPostPartumFu
from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalPostPartumFuAdmin(BaseMaternalModelAdmin):

    form = MaternalPostPartumFuForm
    fields = ('maternal_visit',
              'report_datetime',
              'new_diagnoses',
              'diagnoses',
              'hospitalized',
              'hospitalization_reason',
              'hospitalization_other',
              'hospitalization_days',
              'has_who_dx',
              'who')
    list_display = ('maternal_visit', 'new_diagnoses', 'diagnoses', 'has_who_dx')
    list_filter = ('new_diagnoses', 'diagnoses', 'has_who_dx')
    radio_fields = {'new_diagnoses': admin.VERTICAL,
                    'diagnoses': admin.VERTICAL,
                    'has_who_dx': admin.VERTICAL}
    filter_horizontal = ('who', )

admin.site.register(MaternalPostPartumFu, MaternalPostPartumFuAdmin)
