from edc_base.model.models import BaseUuidModel
from edc_export.models import ExportTrackingFieldsMixin
from edc_identifier.models import BaseIdentifierModel
from edc_sync.models import SyncModelMixin


class OrderIdentifierHistory(BaseIdentifierModel, ExportTrackingFieldsMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_lab'
