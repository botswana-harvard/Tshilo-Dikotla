from edc_dashboard.subject import RegisteredSubjectDashboard
from edc_registration.models import RegisteredSubject

from tshilo_dikotla.constants import INFANT
from td_infant.models import InfantVisit, InfantBirth
from td_lab.models import InfantRequisition
from td_maternal.models import (MaternalLocator, MaternalConsent, MaternalVisit,
                                MaternalEligibility)
from edc_appointment.models.appointment import Appointment
from edc_visit_schedule.models.membership_form import MembershipForm


class InfantDashboard(RegisteredSubjectDashboard):

    view = 'infant_dashboard'
    dashboard_url_name = 'subject_dashboard_url'
    dashboard_name = 'Infant Dashboard'
    urlpattern_view = 'apps.tshilo_dikotla.views'
    template_name = 'infant_dashboard.html'
    urlpatterns = [
        RegisteredSubjectDashboard.urlpatterns[0][:-1] +
        '(?P<appointment_code>{appointment_code})/$'] + RegisteredSubjectDashboard.urlpatterns
    urlpattern_options = dict(
        RegisteredSubjectDashboard.urlpattern_options,
        dashboard_model=RegisteredSubjectDashboard.urlpattern_options['dashboard_model'] + '|infant_birth',
        dashboard_type=INFANT,
        appointment_code='2000|2010|2030|2060|2090|2120')

    def __init__(self, **kwargs):
        super(InfantDashboard, self).__init__(**kwargs)
        self.subject_dashboard_url = 'subject_dashboard_url'
        self.visit_model = InfantVisit
        self.dashboard_type_list = [INFANT]
        self.dashboard_models['registered_subject'] = RegisteredSubject
        self.dashboard_models['infant_birth'] = InfantBirth
        self.dashboard_models['visit'] = InfantVisit
        self.membership_form_category = ['infant_enrollment']
        self._requisition_model = InfantRequisition
        self._locator_model = None
        self._maternal_identifier = None
        self._infant_birth = None

    def get_context_data(self, **kwargs):
        super(InfantDashboard, self).get_context_data(**kwargs)
        self.context.update(
            home='tshilo_dikotla',
            search_name=INFANT,
            title='Infant Dashboard',
            subject_dashboard_url=self.subject_dashboard_url,
            infant_hiv_status=self.infant_hiv_status,
            maternal_consent=self.maternal_consent,
            maternal_eligibility=self.maternal_eligibility,
            local_results=self.render_labs(),
            infant_birth=self.infant_birth, )
        return self.context

    @property
    def appointments(self):
        """Returns all appointments for this registered_subject or just one
        if given a appointment_code and appointment_continuation_count.

        Could show
            one
            all
            only for this membership form category (which is the subject type)
            only those for a given membership form
            only those for a visit definition grouping
            """
        appointments = []
        instruction = self.request.GET.get('instruction', '')
        if self.show == 'forms':
            appointments = [self.appointment]
        else:
            # or filter appointments for the current membership categories
            # schedule__membership_form
            codes = []
            for category in self.membership_form_category:
                codes.extend(MembershipForm.objects.codes_for_category(membership_form_category=category))
                appointments = Appointment.objects.filter(
                    registered_subject=self.registered_subject,
                    visit_definition__code__in=codes,
                    visit_definition__instruction=instruction).order_by(
                    'visit_definition__time_point', 'visit_instance', 'appt_datetime')
        return appointments

    @property
    def instruction(self):
        return 'V' + self.maternal_consent.version

    @property
    def maternal_consent(self):
        return MaternalConsent.objects.filter(subject_identifier=self.maternal_identifier).order_by('-version').first()

    @property
    def subject_identifier(self):
        return self.registered_subject.subject_identifier

    @property
    def maternal_identifier(self):
        return self.registered_subject.relative_identifier

    @RegisteredSubjectDashboard.locator_model.getter
    def locator_model(self):
        return MaternalLocator

    @property
    def locator_visit_model(self):
        return MaternalVisit

    @property
    def locator_registered_subject(self):
        return RegisteredSubject.objects.get(
            subject_identifier=self.maternal_identifier)

    @property
    def maternal_eligibility(self):
        try:
            return MaternalEligibility.objects.get(
                registered_subject__subject_identifier=self.maternal_identifier)
        except MaternalEligibility.DoesNotExist:
            pass

    @property
    def infant_birth(self):
        try:
            self._infant_birth = InfantBirth.objects.get(
                registered_subject__subject_identifier=self.subject_identifier)
        except InfantBirth.DoesNotExist:
            self._infant_birth = None
        return self._infant_birth

    @property
    def registered_subject(self):
        if not self._registered_subject:
            try:
                self._registered_subject = RegisteredSubject.objects.get(pk=self.dashboard_id)
            except RegisteredSubject.DoesNotExist:
                try:
                    self._registered_subject = self.dashboard_model_instance.registered_subject
                except AttributeError:
                    try:
                        self._registered_subject = self.dashboard_model_instance.appointment.registered_subject
                    except AttributeError:
                        try:
                            self._infant_birth = InfantBirth.objects.get(pk=self.dashboard_id)
                            self._registered_subject = self._infant_birth.registered_subject
                        except InfantBirth.DoesNotExist:
                            pass
        return self._registered_subject

    def get_visit_model(self):
        return self.visit_model

    @property
    def infant_hiv_status(self):
        return None
