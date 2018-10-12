from django.contrib import admin

from ..forms import MaternalPostPartumDepForm
from ..models import MaternalPostPartumDep
from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalPostPartumDepAdmin(BaseMaternalModelAdmin):

    form = MaternalPostPartumDepForm
    list_display = ('maternal_visit', 'laugh', 'enjoyment', 'blame')

    fields = ('maternal_visit',
              'report_datetime',
              'laugh',
              'enjoyment',
              'blame',
              'anxious',
              'panick',
              'top',
              'unhappy',
              'sad',
              'crying',
              'self_harm',
              'total_score')

    radio_fields = {'laugh': admin.VERTICAL,
                    'enjoyment': admin.VERTICAL,
                    'blame': admin.VERTICAL,
                    'anxious': admin.VERTICAL,
                    'panick': admin.VERTICAL,
                    'top': admin.VERTICAL,
                    'unhappy': admin.VERTICAL,
                    'sad': admin.VERTICAL,
                    'crying': admin.VERTICAL,
                    'self_harm': admin.VERTICAL}


admin.site.register(MaternalPostPartumDep, MaternalPostPartumDepAdmin)
