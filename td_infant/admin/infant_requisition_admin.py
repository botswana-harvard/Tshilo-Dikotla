from copy import copy

from django.contrib import admin

from edc_lab.modeladmin_mixins import RequisitionAdminMixin

from td.admin_mixins import ModelAdminMixin
from td.constants import INFANT
from td_infant.models import InfantVisit

from ..forms import InfantRequisitionForm
from ..models import InfantRequisition, Panel
from td_infant.models.infant_crf_model import InfantCrfModel


@admin.register(InfantRequisition)
class InfantRequisitionAdmin(InfantCrfModel, RequisitionAdminMixin, admin.ModelAdmin):

    form = InfantRequisitionForm
