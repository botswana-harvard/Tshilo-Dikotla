from django.contrib import admin

from edc_export.actions import export_as_csv_action
from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin
# from lis.labeling.actions import print_aliquot_label
from edc_label.actions import print_labels
from ..actions import create_order, reject_aliquot_label
from ..classes.aliquot_label import print_aliquot_label
from ..models import Aliquot
from edc_lab.lab_aliquot.admin import AliquotModelAdminMixin


@admin.register(Aliquot)
class AliquotAdmin(AliquotModelAdminMixin, MembershipBaseModelAdmin, admin.ModelAdmin):

    actions = [print_labels, create_order, reject_aliquot_label,
               export_as_csv_action(
                   "Export as csv", fields=[], delimiter=',',
                   exclude=['id', 'revision', 'hostname_created',
                            'hostname_modified', 'user_created', 'user_modified'],)]
