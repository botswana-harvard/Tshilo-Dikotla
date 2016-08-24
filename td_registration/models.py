from edc_base.model.models import BaseUuidModel
from edc_registration.models import RegisteredSubjectModelMixin
from edc_sync.models import SyncHistoricalRecords, SyncModelMixin


class RegisteredSubject(SyncModelMixin, RegisteredSubjectModelMixin, BaseUuidModel):

    history = SyncHistoricalRecords()

    class Meta:
        app_label = 'td_registration'
