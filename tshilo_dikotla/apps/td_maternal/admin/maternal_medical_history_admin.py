from django.contrib import admin

from ..forms import MaternalMedicalHistoryForm
from ..models import MaternalMedicalHistory
from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalMedicalHistoryAdmin(BaseMaternalModelAdmin):

    form = MaternalMedicalHistoryForm
#     fields = ('maternal_visit',
#               'chronic_since',
# #               'chronic',
#               'chronic_other',
#               'who_diagnosis',
# #               'who',
#     )
    list_display = ('maternal_visit', 'chronic_since', 'sero_posetive', 'date_hiv_diagnosis', 'perinataly_infected')
    list_filter = ('chronic_since', 'sero_posetive', 'date_hiv_diagnosis', 'perinataly_infected')
    radio_fields = {'chronic_since': admin.VERTICAL,
                    'who_diagnosis': admin.VERTICAL,
                    'sero_posetive': admin.VERTICAL,
                    'perinataly_infected': admin.VERTICAL,
                    'know_hiv_status': admin.VERTICAL}
    filter_horizontal = ('who', 'mother_chronic', 'father_chronic', 'mother_medications')

admin.site.register(MaternalMedicalHistory, MaternalMedicalHistoryAdmin)
