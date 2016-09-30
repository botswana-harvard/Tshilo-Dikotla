from django.contrib import admin

from ..forms import MaternalPostPartumDepForm
from ..models import MaternalPostPartumDep
from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(MaternalPostPartumDep)
class MaternalPostPartumDepAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalPostPartumDepForm
    list_display = ('maternal_visit', 'laugh', 'enjoyment', 'blame')
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
