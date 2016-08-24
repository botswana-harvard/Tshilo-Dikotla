from django.contrib import admin

from edc_lab.lab_aliquot.admin import AliquotTypeModelAdminMixin

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin

from ..models import AliquotType


@admin.register(AliquotType)
class AliquotTypeAdmin(AliquotTypeModelAdminMixin, MembershipBaseModelAdmin, admin.ModelAdmin):
    pass
