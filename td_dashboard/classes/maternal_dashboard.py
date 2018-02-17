from collections import OrderedDict
from django.utils import timezone

from edc_registration.models import RegisteredSubject
from edc_base.utils import convert_from_camel
from edc_constants.constants import YES, POS, NEG, IND, NEVER, UNKNOWN, DWTA, OTHER
from edc_dashboard.subject import RegisteredSubjectDashboard

from tshilo_dikotla.constants import INFANT
from td_lab.models import MaternalRequisition
from td_maternal.models import (
    MaternalVisit, MaternalEligibility, MaternalConsent, MaternalLocator,
    AntenatalEnrollment, MaternalLabourDel, EnrollmentHelper, MaternalRando)
from td_infant.models import InfantBirth
from td_maternal.classes import MaternalStatusHelper
from edc_visit_schedule.models.membership_form import MembershipForm
from edc_appointment.models.appointment import Appointment


UNK = 'unk'


class MaternalDashboard(RegisteredSubjectDashboard):

    view = 'maternal_dashboard'
    dashboard_url_name = 'subject_dashboard_url'
    dashboard_name = 'Maternal Dashboard'
    urlpattern_view = 'apps.td_dashboard.views'
    template_name = 'maternal_dashboard.html'
    urlpatterns = [
        RegisteredSubjectDashboard.urlpatterns[0][:-1] +
        '(?P<appointment_code>{appointment_code})/$'] + RegisteredSubjectDashboard.urlpatterns
    urlpattern_options = dict(
        RegisteredSubjectDashboard.urlpattern_options,
        dashboard_model=RegisteredSubjectDashboard.urlpattern_options['dashboard_model'] + '|maternal_eligibility',
        dashboard_type='maternal',
        appointment_code='1000M|1100M|1200M|1600M|2200M|2800M|3400M|4000M|4600M', )

    def __init__(self, **kwargs):
        super(MaternalDashboard, self).__init__(**kwargs)
        self.subject_dashboard_url = 'subject_dashboard_url'
        self.visit_model = MaternalVisit
        self.dashboard_type_list = ['maternal']
        self.membership_form_category = ['specimen', 'enrollment', 'antenatal', 'follow_up']
        self.dashboard_models['maternal_eligibility'] = MaternalEligibility
        self.dashboard_models['maternal_consent'] = MaternalConsent
        self.dashboard_models['visit'] = MaternalVisit
        self._requisition_model = MaternalRequisition
        self._locator_model = MaternalLocator
        self.maternal_status_helper = None

    def get_context_data(self, **kwargs):
        super(MaternalDashboard, self).get_context_data(**kwargs)
        self.context.update(
            home='tshilo_dikotla',
            search_name='maternal',
            title='Maternal Dashboard',
            subject_dashboard_url=self.subject_dashboard_url,
            infants=self.get_registered_infant_identifier(),
            maternal_consent=self.consent,
            local_results=self.render_labs(),
            antenatal_enrollment=self.antenatal_enrollment,
            enrollment_hiv_status=self.maternal_status_helper.enrollment_hiv_status,
            current_hiv_status=self.maternal_status_helper.hiv_status,
            currently_pregnant=self.currently_pregnant,
            gestational_age=self.gestational_age,
            planned_delivery_site=self.planned_delivery_site,
            delivery_site=self.delivery_site,
            maternal_eligibility=self.maternal_eligibility,
            randomized=self.randomized
        )
        return self.context

    @property
    def maternal_eligibility(self):
        try:
            return MaternalEligibility.objects.get(
                registered_subject__subject_identifier=self.subject_identifier)
        except MaternalEligibility.DoesNotExist:
            pass

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
        instruction = self.request.GET.get('instruction', self.instruction)
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
                    visit_definition__instruction__in=[instruction, 'V1_V3']).order_by(
                    'visit_definition__time_point', 'visit_instance', 'appt_datetime')
        return appointments

    @property
    def instruction(self):
        return 'V' + self.consent.version

    @property
    def consent(self):
        self._consent = None
        try:
            self._consent = MaternalConsent.objects.filter(
                subject_identifier=self.subject_identifier).order_by('-version').first()
        except MaternalConsent.DoesNotExist:
            self._consent = None
        return self._consent

    @property
    def randomized(self):
        try:
            randomization = MaternalRando.objects.get(
                maternal_visit__appointment__registered_subject__subject_identifier=self.subject_identifier)
            return randomization.rx
        except MaternalRando.DoesNotExist:
            return None

    @property
    def latest_visit(self):
        return self.visit_model.objects.filter(
            appointment__registered_subject=self.registered_subject).order_by(
                '-appointment__visit_definition__time_point').first()

    def get_locator_scheduled_visit_code(self):
        """ Returns visit where the locator is scheduled, TODO: maybe search visit definition for this?."""
        return '1000M'

    @property
    def maternal_locator(self):
        return self.locator_model.objects.get(
            registered_subject__subject_identifier=self.subject_identifier)

    @property
    def subject_identifier(self):
        return self.registered_subject.subject_identifier

    @property
    def locator_model(self):
        return MaternalLocator

    def get_registered_infant_identifier(self):
        """Returns an infant identifier associated with the maternal identifier"""
        infants = OrderedDict()
        infant_registered_subject = None
        try:
            infant_registered_subject = RegisteredSubject.objects.get(
                subject_type=INFANT, relative_identifier__iexact=self.subject_identifier)
            try:
                infant_birth = InfantBirth.objects.get(registered_subject__exact=infant_registered_subject)
                dct = infant_birth.__dict__
                dct['dashboard_model'] = convert_from_camel(infant_birth._meta.object_name)
                dct['dashboard_id'] = convert_from_camel(str(infant_birth.pk))
                dct['dashboard_type'] = INFANT
                infants[infant_registered_subject.subject_identifier] = dct
            except InfantBirth.DoesNotExist:
                dct = {'subject_identifier': infant_registered_subject.subject_identifier}
                dct['dashboard_model'] = 'registered_subject'
                dct['dashboard_id'] = str(infant_registered_subject.pk)
                dct['dashboard_type'] = INFANT
                infants[infant_registered_subject.subject_identifier] = dct
        except RegisteredSubject.DoesNotExist:
            pass
        return infants

    @property
    def antenatal_enrollment(self):
        if not self.maternal_status_helper:
            self.maternal_status_helper = MaternalStatusHelper(self.latest_visit)
        try:
            antenatal_enrollment = AntenatalEnrollment.objects.get(registered_subject=self.registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            antenatal_enrollment = None
        return antenatal_enrollment

    @property
    def maternal_randomization(self):
        if not self.maternal_status_helper:
            self.maternal_status_helper = MaternalStatusHelper(self.latest_visit)
        try:
            maternal_rando = MaternalRando.objects.get(
                maternal_visit__appointment__registered_subject=self.registered_subject)
        except MaternalRando.DoesNotExist:
            maternal_rando = None
        return maternal_rando

    @property
    def maternal_delivery(self):
        if not self.maternal_status_helper:
            self.maternal_status_helper = MaternalStatusHelper(self.latest_visit)
        try:
            delivery = MaternalLabourDel.objects.get(registered_subject=self.registered_subject)
        except MaternalLabourDel.DoesNotExist:
            delivery = None
        return delivery

    @property
    def currently_pregnant(self):
        if not self.maternal_delivery:
            return True
        return None

    @property
    def planned_delivery_site(self):
        if not self.maternal_status_helper:
            self.maternal_status_helper = MaternalStatusHelper(self.latest_visit)
        if self.maternal_randomization and self.maternal_randomization.delivery_clinic != OTHER:
            return self.maternal_randomization.delivery_clinic
        elif self.maternal_randomization and self.maternal_randomization.delivery_clinic == OTHER:
            return self.maternal_randomization.delivery_clinic_other
        else:
            return UNK

    @property
    def delivery_site(self):
        if self.maternal_delivery:
            return (self.maternal_delivery.delivery_hospital if
                    self.maternal_delivery.delivery_hospital != OTHER else
                    self.maternal_delivery.delivery_hospital_other)
        return UNK

    @property
    def gestational_age(self):
        if not self.maternal_status_helper:
            self.maternal_status_helper = MaternalStatusHelper(self.latest_visit)
        antenatal = self.antenatal_enrollment
        if antenatal:
            enrollment_helper = EnrollmentHelper(instance_antenatal=antenatal)
            if enrollment_helper.evaluate_ga_lmp(timezone.datetime.now().date()) and self.currently_pregnant:
                return enrollment_helper.evaluate_ga_lmp(timezone.datetime.now().date())
            elif (not enrollment_helper.evaluate_ga_lmp(timezone.datetime.now().date()) and self.currently_pregnant
                  and antenatal.ultrasound):
                return antenatal.ultrasound.ga_confirmed
            elif enrollment_helper.evaluate_ga_lmp(timezone.datetime.now().date()) and not self.currently_pregnant:
                delivery = self.maternal_delivery
                return enrollment_helper.evaluate_ga_lmp(delivery.delivery_datetime.date())
            else:
                return UNK
        return UNK

