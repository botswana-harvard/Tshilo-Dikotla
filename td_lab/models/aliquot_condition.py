from django.db import models

from lis.specimen.lab_aliquot_list.models import BaseAliquotCondition


class AliquotConditionManager(models.Manager):

    def get_by_natural_key(self, name):
        return self.get(name=name)


class AliquotCondition(BaseAliquotCondition):

    objects = AliquotConditionManager()

    class Meta:
        app_label = 'td_lab'
