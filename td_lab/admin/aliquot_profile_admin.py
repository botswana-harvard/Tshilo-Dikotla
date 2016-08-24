from django.contrib import admin

from edc_base.modeladmin.mixins import TabularInlineMixin
from edc_lab.lab_aliquot.admin import (
    AliquotProfileModelAdminMixin, AliquotProfileItemModelAdminMixin)

from tshilo_dikotla.base_model_admin import MembershipModelAdminMixin

from ..models import AliquotProfileItem, AliquotProfile


@admin.register(AliquotProfileItem)
class AliquotProfileItemAdmin(AliquotProfileItemModelAdminMixin, admin.ModelAdmin):
    pass


class AliquotProfileItemInlineAdmin(TabularInlineMixin, MembershipModelAdminMixin, admin.TabularInline):
    model = AliquotProfileItem


@admin.register(AliquotProfile)
class AliquotProfileAdmin(AliquotProfileModelAdminMixin, admin.ModelAdmin):
    inlines = [AliquotProfileItemInlineAdmin]
