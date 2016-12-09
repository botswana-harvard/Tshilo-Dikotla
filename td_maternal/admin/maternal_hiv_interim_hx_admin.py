from django.contrib import admin

from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin

from td.admin_mixins import ModelAdminMixin

from ..admin_site import td_maternal_admin
from ..forms import MaternalHivInterimHxForm
from ..models import MaternalHivInterimHx


@admin.register(MaternalHivInterimHx, site=td_maternal_admin)
class MaternalHivInterimHxAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    form = MaternalHivInterimHxForm

    radio_fields = {'has_cd4': admin.VERTICAL,
                    'has_vl': admin.VERTICAL,
                    'vl_detectable': admin.VERTICAL}
