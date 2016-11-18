from edc_base.model.models import BaseUuidModel
from edc_export.model_mixins import ExportTrackingFieldsMixin
from edc_identifier.models import BaseIdentifierModel
from edc_base.model.models import HistoricalRecords


class OrderIdentifierHistory(BaseIdentifierModel, ExportTrackingFieldsMixin, BaseUuidModel):

    history = HistoricalRecords()

    class Meta:
        app_label = 'td_lab'
