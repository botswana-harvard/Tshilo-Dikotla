from django.contrib import admin

from td.admin_mixins import ModelAdminMixin

from ..forms import MaternalEligibilityForm
from ..models import MaternalEligibility
from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin


@admin.register(MaternalEligibility)
class MaternalEligibilityAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    form = MaternalEligibilityForm

    fields = ('reference',
              'report_datetime',
              'age_in_years',
              'has_omang')

    radio_fields = {'has_omang': admin.VERTICAL}

    readonly_fields = ('reference',)

    list_display = ('report_datetime', 'age_in_years', 'is_eligible')

    list_filter = ('report_datetime', 'is_eligible')
