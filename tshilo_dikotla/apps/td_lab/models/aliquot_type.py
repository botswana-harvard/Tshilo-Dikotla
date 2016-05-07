from django.db import models

from lis.specimen.lab_aliquot_list.models import BaseAliquotType


class AliquotTypeManager(models.Manager):

    def get_by_natural_key(self, alpha_code, numeric_code):
        return self.get(alpha_code=alpha_code, numeric_code=numeric_code)


class AliquotType(BaseAliquotType):

    objects = AliquotTypeManager()

    class Meta:
        app_label = 'td_lab'
        ordering = ["name"]
