from edc_base.model.models import BaseUuidModel
from edc_metadata.model_mixins import CrfMetadataModelMixin
from django.urls.base import reverse
from django.apps import apps
from td.models import Appointment


class CrfMetadata(CrfMetadataModelMixin, BaseUuidModel):

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
    def crf_model_add_or_update(self):
        app_label, model_name = self.model.split('.')
        model = apps.get_app_config('td_maternal').get_model(model_name)
        obj = None
        try:
            obj = model.objects.get(maternal_visit__appointment__subject_identifier=self.subject_identifier)
            admin_model_url_label = model._meta.verbose_name
            admin_model_change_url = obj.get_absolute_url()
            return (admin_model_url_label, admin_model_change_url)
        except model.DoesNotExist:
            admin_model_url_label = model._meta.verbose_name
            admin_model_add_url = reverse('admin:{}_{}_add'.format(app_label, model_name))
            return (admin_model_url_label, admin_model_add_url)

    class Meta(CrfMetadataModelMixin.Meta):
        app_label = 'td_maternal'
