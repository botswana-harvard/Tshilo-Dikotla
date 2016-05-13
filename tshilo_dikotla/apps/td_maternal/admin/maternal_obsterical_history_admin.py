from django.contrib import admin

from ..forms import MaternalObstericalHistoryForm
from ..models import MaternalObstericalHistory

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalObstericalHistoryAdmin(BaseMaternalModelAdmin):

    form = MaternalObstericalHistoryForm
    fields = ('maternal_visit',
              'prev_pregnancies',
              'pregs_24wks_or_more',
              'lost_before_24wks',
              'lost_after_24wks',
              'live_children',
              'children_died_b4_5yrs')
    list_display = ('maternal_visit',
                    'prev_pregnancies',
                    'pregs_24wks_or_more',
                    'lost_before_24wks',
                    'lost_after_24wks',
                    'live_children')

admin.site.register(MaternalObstericalHistory, MaternalObstericalHistoryAdmin)
