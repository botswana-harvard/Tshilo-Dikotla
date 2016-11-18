from django.contrib import admin

from edc_export.actions import export_as_csv_action
from tshilo_dikotla.admin_mixins import EdcBaseModelAdminMixin
# from lis.labeling.actions import print_aliquot_label
from edc_label.actions import print_labels_action
# from ..actions import create_order, reject_aliquot_label
# from ..classes.aliquot_label import print_aliquot_label
from ..models import Aliquot
from edc_lab.modeladmin_mixins import AliquotModelAdminMixin


@admin.register(Aliquot)
class AliquotAdmin(AliquotModelAdminMixin, EdcBaseModelAdminMixin, admin.ModelAdmin):

    actions = [print_labels_action,  # create_order, reject_aliquot_label,
               export_as_csv_action(
                   "Export as csv", fields=[], delimiter=',',
                   exclude=['id', 'revision', 'hostname_created',
                            'hostname_modified', 'user_created', 'user_modified'],)]

    @property
    def subject_identifier(self):
        pass

    @property
    def is_packed(self):
        pass

    @property
    def to_receive(self):
        pass

    @property
    def drawn(self):
        pass

    @property
    def aliquot_condition(self):
        pass
