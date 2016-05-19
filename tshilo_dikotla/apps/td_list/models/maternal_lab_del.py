from edc_base.model.models import BaseListModel
from edc_code_lists.models import DxCode


class HealthCond (BaseListModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal LabDel: Health Cond"


class DelComp (BaseListModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal LabDel: Delivery Comp"


class ObComp(BaseListModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal LabDel: Ob Comp"


class LabDelDx (DxCode):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal LabDel: Dx"
