from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_metadata.model_mixins import RequisitionMetadataModelMixin
from django.urls.base import reverse
from django.apps.registry import apps
from td_appointment.models import Appointment


class RequisitionMetadata(RequisitionMetadataModelMixin, BaseUuidModel):

    @property
    def appointment(self):
        appt = None
        try:
            appt = Appointment.objects.get(
                visit_code=self.visit_code, subject_identifier=self.subject_identifier)
        except Appointment.DoesNotExist:
            return appt
        return appt

    @property
    def reqs_model_add_or_update(self):
        app_label, model_name = self.model.split('.')
        model = apps.get_app_config('td_lab').get_model(model_name)
        obj = None
        try:
            obj = model.objects.get(
                maternal_visit__appointment__subject_identifier=self.subject_identifier,
                panel_name=self.panel_name,
                maternal_visit__appointment__visit_code=self.visit_code)
            admin_model_url_label = model._meta.verbose_name
            admin_model_change_url = obj.get_absolute_url()
            return (admin_model_url_label, admin_model_change_url)
        except model.DoesNotExist:
            admin_model_url_label = model._meta.verbose_name
            admin_model_add_url = reverse('admin:{}_{}_add'.format(app_label, model_name))
            return (admin_model_url_label, admin_model_add_url)

    class Meta(RequisitionMetadataModelMixin.Meta):
        app_label = 'td_maternal'
