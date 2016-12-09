from django.contrib import admin

from ..admin_site import td_maternal_admin
from ..forms import MaternalObstericalHistoryForm
from ..models import MaternalObstericalHistory

from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(MaternalObstericalHistory, site=td_maternal_admin)
class MaternalObstericalHistoryAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalObstericalHistoryForm
    fields = ('maternal_visit',
              'report_datetime',
              'prev_pregnancies',
              'pregs_24wks_or_more',
              'lost_before_24wks',
              'lost_after_24wks',
              'live_children',
              'children_died_b4_5yrs',
              'children_deliv_before_37wks',
              'children_deliv_aftr_37wks')
    list_display = ('maternal_visit',
                    'prev_pregnancies',
                    'pregs_24wks_or_more',
                    'lost_before_24wks',
                    'lost_after_24wks',
                    'live_children')
