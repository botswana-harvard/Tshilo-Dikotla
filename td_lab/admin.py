from django.contrib import admin

from td_infant.admin.admin_mixins import CrfModelAdminMixin as InfantCrfModelAdminMixin
from td_maternal.admin.admin_mixins import CrfModelAdminMixin as MaternalCrfModelAdminMixin

from .forms import InfantRequisitionForm, MaternalRequisitionForm
from .models import InfantRequisition, MaternalRequisition


@admin.register(InfantRequisition)
class InfantRequisitionAdmin(InfantCrfModelAdminMixin, admin.ModelAdmin):

    form = InfantRequisitionForm


@admin.register(MaternalRequisition)
class MaternalRequisitionAdmin(MaternalCrfModelAdminMixin, admin.ModelAdmin):

    form = MaternalRequisitionForm
