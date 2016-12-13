from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel

# from edc_lab.lab_clinic_api.choices import PANEL_TYPE
# from edc_lab.lab_clinic_api.models import TestCode
#
# from edc_lab.lab_panel.models import BasePanel
#
# from .aliquot_type import AliquotType

from ..managers import PanelManager


class Panel(BaseUuidModel):

    name = models.CharField(max_length=25)

#     test_code = models.ManyToManyField(TestCode, blank=True, related_name='+')
#
#     aliquot_type = models.ManyToManyField(
#         AliquotType,
#         help_text='Choose all that apply',)
#
#     panel_type = models.CharField(max_length=15, choices=PANEL_TYPE, default='TEST')
#
    objects = PanelManager()

    def natural_key(self):
        return (self.name, )

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'td_lab'
