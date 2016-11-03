from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from ..classes import MarqueeViewMixin
from td_maternal.models.maternal_consent import MaternalConsent
from td_maternal.models.maternal_locator import MaternalLocator
from tshilo_dikotla.constants import INFANT
from td_infant.models.infant_visit import InfantVisit
from _collections import OrderedDict
from td_infant.models.infant_birth import InfantBirth
from td_dashboard.classes.dashboard_mixin import DashboardMixin
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class InfantDashboardView(
        MarqueeViewMixin, EdcBaseViewMixin, DashboardMixin, TemplateView):

    def __init__(self, **kwargs):
        super(InfantDashboardView, self).__init__(**kwargs)
        self.request = None
        self.context = {}
        self.show = None
        self._crfs = []
        self._requisitions = []
        self._appointments = None
        self.maternal_status_helper = None
        self.dashboard = 'td_infant'
        self.template_name = 'td_dashboard/infant/subject_dashboard.html'
        self._selected_appointment = None
        self.enrollments_models = [
            'td_infant.infantbirth'
        ]

    def get_context_data(self, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
            site_header=admin.site.site_header,
        )
        self.context.update({
            'demographics': self.demographics,
            'markey_next_row': self.markey_next_row,
            'requisitions': self.requisitions,
            'crfs': self.crfs,
            'enrollments': self.enrollments,
            'appointments': self.appointments,
            'dashboard_url': self.dashboard_url,
            'selected_appointment': self.selected_appointment,
            'subject_identifier': self.subject_identifier,
            'dashboard_url': self.dashboard_url,
            'consents': [],
            'consent': self.consent,
            'dashboard_type': INFANT,
            'locator': self.locator,
        })
        return self.context

    def get(self, request, *args, **kwargs):
        self.request = request
        context = self.get_context_data(**kwargs)
        self.show = request.GET.get('show', None)
        context.update({'show': self.show})
        return self.render_to_response(context)

    @property
    def locator(self):
        maternal_subject_identifier = self.subject_identifier[:-3] if self.subject_identifier else ''
        try:
            maternal_locator = MaternalLocator.objects.get(
                registered_subject__subject_identifier=maternal_subject_identifier)
        except MaternalLocator.DoesNotExist:
            maternal_locator = None
        return maternal_locator

    @property
    def demographics(self):
        demographics = OrderedDict()
        name = '{}({})'.format(self.infant_birth.first_name, self.infant_birth.initials) if self.infant_birth else ''
        dob = self.infant_birth.dob if self.infant_birth else ''
        demographics['Name'] = name,
        demographics['Born'] = dob,
        demographics['Age'] = str(relativedelta(timezone.now().date(), dob).years)
        demographics.update({'Hiv status': '?'})
        return demographics

    @property
    def infant_birth(self):
        try:
            self._infant_birth = InfantBirth.objects.get(
                registered_subject__subject_identifier=self.subject_identifier)
        except InfantBirth.DoesNotExist:
            self._infant_birth = None
        return self._infant_birth

    @property
    def latest_visit(self):
        return InfantVisit.objects.filter(
            appointment__subject_identifier=self.subject_identifier).order_by(
                '-created').first()

    @property
    def consent(self):
        try:
            maternal_subject_identifier = self.subject_identifier[:-3] if self.subject_identifier else ''
            maternal_consent = MaternalConsent.objects.get(subject_identifier=maternal_subject_identifier)
        except MaternalConsent.DoesNotExist:
            maternal_consent = None
        return maternal_consent

    @property
    def show_forms(self):
        show = self.request.GET.get('show', None)
        return True if show == 'forms' else False
