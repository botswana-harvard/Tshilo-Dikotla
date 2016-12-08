from django.contrib import admin

from ..admin_site import td_maternal_admin
from ..forms import MaternalUltraSoundFuForm
from ..models import MaternalUltraSoundFu

from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(MaternalUltraSoundFu, site=td_maternal_admin)
class MaternalUltraSoundFuAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):

    form = MaternalUltraSoundFuForm

    fields = ('maternal_visit',
              'report_datetime',
              'bpd',
              'hc',
              'ac',
              'fl')

    list_display = ('maternal_visit', 'report_datetime')

    list_filter = ('report_datetime', )
