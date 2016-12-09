from collections import OrderedDict
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import localtime
from django.views.generic import TemplateView

from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin

from td.constants import INFANT
from td_infant.models import InfantBirth, InfantVisit
from td_maternal.models import MaternalConsent, MaternalLocator

from edc_dashboard.view_mixins import DashboardMixin


class InfantDashboardView(EdcBaseViewMixin, DashboardMixin, TemplateView):

    def __init__(self, **kwargs):
        super(InfantDashboardView, self).__init__(**kwargs)
        self.request = None
        self.show = None
        self._crfs = []
        self._requisitions = []
        self._appointments = None
        self.maternal_status_helper = None
        self.dashboard = 'td_infant'
        self.template_name = 'td_dashboard/subject_dashboard.html'
        self._selected_appointment = None
        self.enrollments_models = ['td_infant.infantbirth']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InfantDashboardView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        self.context = super(InfantDashboardView, self).get_context_data(**kwargs)
        self.context.update({
            'appointments': self.appointments,
            'consent': self.consent,
            'consents': [],
            'crfs': self.crfs,
            'dashboard_type': INFANT,
            'dashboard_url': self.dashboard_url,
            'dashboard_url': self.dashboard_url,
            'demographics': self.demographics,
            'enrollments': self.enrollments,
            'locator': self.locator,
            'requisitions': self.requisitions,
            'selected_appointment': self.selected_appointment,
            'subject_identifier': self.subject_identifier,
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
        demographics['Age'] = str(relativedelta(localtime(get_utcnow()).date(), dob).years)
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
