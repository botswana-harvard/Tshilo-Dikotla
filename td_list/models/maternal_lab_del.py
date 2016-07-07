from edc_base.model.models import ListModelMixin
from edc_code_lists.models import DxCode


class HealthCond (ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal LabDel: Health Cond"


class DelComp (ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal LabDel: Delivery Comp"


class ObComp(ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal LabDel: Ob Comp"


class LabDelDx (DxCode):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal LabDel: Dx"
