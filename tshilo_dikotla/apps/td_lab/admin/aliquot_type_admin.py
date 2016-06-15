from django.contrib import admin

from tshilo_dikotla.apps.td.base_model_admin import MembershipBaseModelAdmin

from ..models import AliquotType


class AliquotTypeAdmin(MembershipBaseModelAdmin):

    list_display = ('name', 'alpha_code', 'numeric_code')

admin.site.register(AliquotType, AliquotTypeAdmin)
