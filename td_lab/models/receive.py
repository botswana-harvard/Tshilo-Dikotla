from django.core.urlresolvers import reverse
from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_export.models import ExportTrackingFieldsMixin
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords

from lis.specimen.lab_receive.models import BaseReceive

from ..managers import ReceiveManager


class Receive(BaseReceive, SyncModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    registered_subject = models.ForeignKey(RegisteredSubject, null=True, related_name='tshilo_dikotla_receive')

    requisition_model_name = models.CharField(max_length=25, null=True, editable=False)

    subject_type = models.CharField(max_length=25, null=True, editable=False)

    objects = ReceiveManager()

    history = SyncHistoricalRecords()

    def save(self, *args, **kwargs):
        self.subject_type = self.registered_subject.subject_type
        super(Receive, self).save(*args, **kwargs)

    def __str__(self):
        return self.receive_identifier or u''

    def deserialize_get_missing_fk(self, attrname):
        retval = None
        return retval

    def requisition(self):
        url = reverse('admin:td_lab_maternalrequisition_changelist')
        return '<a href="{0}?q={1}">{1}</a>'.format(url, self.requisition_identifier)
    requisition.allow_tags = True

    def natural_key(self):
        return (self.receive_identifier, )

    class Meta:
        app_label = 'td_lab'
