from django.contrib import admin

from ..forms import MaternalMedicalHistoryForm
from ..models import MaternalMedicalHistory
from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalMedicalHistoryAdmin(BaseMaternalModelAdmin):

    form = MaternalMedicalHistoryForm
    fields = ('maternal_visit',
              'chronic_since',
#               'chronic',
              'chronic_other',
              'who_diagnosis',
#               'who',
    )
    list_display = ('maternal_visit', 'chronic_since', )
    list_filter = ('chronic_since', )
    radio_fields = {'chronic_since': admin.VERTICAL,
                    'who_diagnosis': admin.VERTICAL}
#     filter_horizontal = ('chronic', 'who',)

admin.site.register(MaternalMedicalHistory, MaternalMedicalHistoryAdmin)
