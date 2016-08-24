from edc_lab.lab_aliquot.model_mixins import AliquotConditionModelMixin
from edc_lab.lab_aliquot.managers import AliquotConditionManager


class AliquotCondition(AliquotConditionModelMixin):

    objects = AliquotConditionManager()

    class Meta:
        app_label = 'td_lab'
