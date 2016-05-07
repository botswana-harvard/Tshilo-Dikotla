from django.core.urlresolvers import reverse
from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_export.models import ExportTrackingFieldsMixin
from edc_sync.models import SyncModelMixin
from lis.specimen.lab_result.models import BaseResult

#from ..managers import ResultManager

from .order_item import OrderItem


class Result(BaseResult, ExportTrackingFieldsMixin, BaseUuidModel):
    """Stores result information in a one-to-many relation with :class:`ResultItem`."""
    order_item = models.ForeignKey(OrderItem)

    subject_identifier = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        db_index=True,
        help_text="non-user helper field to simplify search and filtering")

    #objects = ResultManager()
    objects = models.Manager()

    #history = AuditTrail()

    def save(self, *args, **kwargs):
        self.subject_identifier = self.order.aliquot.receive.registered_subject.subject_identifier
        super(Result, self).save(*args, **kwargs)

    def panel(self):
        try:
            return str(self.order_item.panel.edc_name)
        except AttributeError:
            return None

    def natural_key(self):
        return (self.result_identifier, self.subject_identifier)

    def report(self):
        url = reverse('view_result_report', kwargs={'result_identifier': self.result_identifier})
        url_review = reverse('admin:lab_clinic_api_review_add')
        two = ''
        if self.review:
            label = 'comment'
            url_review = self.review.get_absolute_url()
            two = ('<a href="{url}" class="add-another" id="add_id_review" '
                   'onclick="return showAddAnotherPopup(this);"> {label}</a>').format(url=url_review, label=label)
        one = ('<a href="{url}" class="add-another" id="add_id_report" '
               'onclick="return showAddAnotherPopup(this);"> <img src="/static/admin/img/icon_addlink.gif" '
               'width="10" height="10" alt="View report"/></a>').format(url=url)
        return '{one}&nbsp;{two}'.format(one=one, two=two)
    report.allow_tags = True

    class Meta:
        app_label = 'td_lab'
        ordering = ['result_identifier']
