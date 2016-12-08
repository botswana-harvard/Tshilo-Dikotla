from django.contrib import admin

from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin

from td.admin_mixins import ModelAdminMixin

from ..admin_site import td_maternal_admin
from ..forms import MaternalEligibilityForm
from ..models import MaternalEligibility


@admin.register(MaternalEligibility, site=td_maternal_admin)
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
