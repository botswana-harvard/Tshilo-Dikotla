from collections import OrderedDict
from dateutil.relativedelta import relativedelta

from django.apps import apps
from django.urls.base import reverse

from edc_base.utils import get_utcnow

from td_maternal.models.maternal_crf_meta_data import CrfMetadata
from td_maternal.models.requisition_meta_data import RequisitionMetadata
from td.models import Appointment


class DashboardMixin(object):

    def __init__(self):
        self._appointments = []
        self.selected_appointment = None
        self._selected_appointment = None
        self.context = {}
        self._crfs = []
        self._requisitions = []
        self.dashboard = None

    @property
    def demographics_data(self):
        return {}

    @property
    def appointments(self):
        if not self._appointments:
            try:
                self._appointments = [Appointment.objects.get(pk=self.kwargs.get('appointment_pk'))]
            except Appointment.DoesNotExist:
                self._appointments = Appointment.objects.filter(
                    subject_identifier=self.subject_identifier).order_by('visit_code')
        return self._appointments

    @property
    def selected_appointment(self):
        if not self._selected_appointment:
            try:
                self._selected_appointment = Appointment.objects.get(pk=self.kwargs.get('appointment_pk'))
            except Appointment.DoesNotExist:
                self._selected_appointment = None
        return self._selected_appointment

    @property
    def dashboard_url(self):
        try:
            dashboard_url = 'subject_dashboard_url' if self.dashboard == 'td_maternal' else 'infant_subject_dashboard_url'
            dashboard_url = reverse(
                dashboard_url,
                kwargs={
                    'subject_identifier': self.subject_identifier,
                    'appointment_pk': self.selected_appointment.pk})
        except AttributeError:
            dashboard_url = None
        return dashboard_url

    @property
    def subject_identifier(self):
        return self.context.get('subject_identifier')

    @property
    def crfs(self):
        if not self._crfs:
            if self.selected_appointment:
                self._crfs = []
                crfs = CrfMetadata.objects.filter(
                    subject_identifier=self.subject_identifier,
                    visit_code=self.selected_appointment.visit_code).order_by('show_order')
                for crf in crfs:
                    try:
                        obj = None
                        if self.dashboard == 'td_maternal':
                            obj = crf.model_class.objects.get(
                                maternal_visit__appointment=self.selected_appointment)
                        else:
                            obj = crf.model_class.objects.get(
                                infant_visit__appointment=self.selected_appointment)
                        crf.instance = obj
                        crf.url = obj.get_absolute_url()
                        crf.title = obj._meta.verbose_name
                    except crf.model_class.DoesNotExist:
                        crf.instance = None
                        crf.url = crf.model_class().get_absolute_url()
                        crf.title = crf.model_class()._meta.verbose_name
                    self._crfs.append(crf)
        return self._crfs

    @property
    def requisitions(self):
        requisitions = None
        if self.selected_appointment:
            self._requisitions = []
            requisitions = RequisitionMetadata.objects.filter(
                subject_identifier=self.subject_identifier, visit_code=self.selected_appointment.visit_code)
            for requisition in requisitions:
                try:
                    obj = None
                    if self.dashboard == 'td_maternal':
                        obj = requisition.model_class.objects.get(
                            maternal_visit__appointment=self.selected_appointment, panel_name=requisition.panel_name)
                    else:
                        obj = requisition.model_class.objects.get(
                            infant_visit__appointment=self.selected_appointment, panel_name=requisition.panel_name)
                    requisition.instance = obj
                    requisition.url = obj.get_absolute_url()
                    requisition.title = obj._meta.verbose_name
                except requisition.model_class.DoesNotExist:
                    requisition.instance = None
                    requisition.url = requisition.model_class().get_absolute_url()
                    requisition.title = requisition.model_class()._meta.verbose_name
                self._requisitions.append(requisition)
        return self._requisitions

    def enrollments(self):
        """ """
        self._subject_membership_models = []
        for model_lower in self.enrollments_models:
            app_label, model_name = model_lower.split('.')
            model = apps.get_app_config(self.dashboard).get_model(model_name)
            obj = None
            try:
                obj = model.objects.get(registered_subject__subject_identifier=self.subject_identifier)
                admin_model_url_label = "{}({})".format(model._meta.verbose_name, 'complete')
                admin_model_change_url = obj.get_absolute_url()
                self._subject_membership_models.append([admin_model_url_label, admin_model_change_url])
            except model.DoesNotExist:
                admin_model_url_label = "{}({})".format(model._meta.verbose_name, 'new')
                admin_model_add_url = reverse('admin:{}_{}_add'.format(app_label, model_name))
                self._subject_membership_models.append([admin_model_url_label, admin_model_add_url])
        return self._subject_membership_models


class MarqueeViewMixin:

    def __init__(self):
        self.context = {}
        self.markey_next_row = 4
        self.consent_model = None
        self.enrollments_models = []
        self.dashboard = None

    def get_context_data(self, **kwargs):
        self.context = super(MarqueeViewMixin, self).get_context_data(**kwargs)
        return self.context

    @property
    def demographics(self):
        demographics = OrderedDict()
        if self.consent:
            demographics['Name'] = '{}({})'.format(self.consent.first_name, self.consent.initials),
            demographics['Born'] = self.consent.dob,
            demographics['Age'] = self.age,
            demographics['Consented'] = self.consent.consent_datetime,
            demographics['Antenatal enrollment status'] = self.demographics_data.get('antenatal_enrollment_status'),
            demographics['Enrollment HIV status'] = self.demographics_data.get('enrollment_hiv_status'),
            demographics['Current HIV status'] = self.demographics_data.get('current_hiv_status'),
            demographics['Pregnant, GA'] = self.demographics_data.get('gestational_age'),
            demographics['Planned delivery site'] = self.demographics_data.get('delivery_site'),
            demographics['Randomized'] = (self.demographics_data.get('randomized'),)
        return demographics

    @property
    def demographics_data(self):
        return {}

    @property
    def consent(self):
        return self.consent_model

    @property
    def age(self):
        return relativedelta(get_utcnow().date(), self.consent.dob).years
