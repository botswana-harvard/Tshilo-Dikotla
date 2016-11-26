from collections import OrderedDict

from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.utils import timezone

from edc_base.utils import convert_from_camel
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import UNK, OTHER

from td_dashboard.classes.dashboard_mixin import DashboardMixin
from td_infant.models.infant_birth import InfantBirth
from td_maternal.classes.maternal_status_helper import MaternalStatusHelper
from td_maternal.models import (
    EnrollmentHelper, AntenatalEnrollment, MaternalConsent, MaternalLabourDel, MaternalLocator,
    MaternalRando, MaternalVisit)
from td.models import RegisteredSubject
from tshilo_dikotla.constants import MATERNAL, INFANT

from ..classes import MarqueeViewMixin


class MaternalDashboardView(
        MarqueeViewMixin, DashboardMixin, EdcBaseViewMixin, TemplateView):

    def __init__(self, **kwargs):
        super(MaternalDashboardView, self).__init__(**kwargs)
        self.request = None
        self.context = {}
        self.show = None
        self.maternal_status_helper = None
        self._crfs = []
        self._selected_appointment = None
        self._appointments = None
        self._requisitions = []
        self.dashboard = 'td_maternal'
        self.template_name = 'td_dashboard/maternal/subject_dashboard.html'
        self.enrollments_models = [
            'td_maternal.specimenconsent', 'td_maternal.antenatalenrollment',
            'td_maternal.antenatalvisitmembership', 'td_maternal.maternallabourdel']

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
            'selected_appointment': self.selected_appointment,
            'appointments': self.appointments,
            'subject_identifier': self.subject_identifier,
            'consents': [],
            'dashboard_type': MATERNAL,
            'locator': self.locator,
            'dashboard_url': self.dashboard_url,
            'enrollments': self.enrollments(),
            'infants': self.get_registered_infant_identifier
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
        try:
            maternal_locator = MaternalLocator.objects.get(
                registered_subject__subject_identifier=self.subject_identifier)
        except MaternalLocator.DoesNotExist:
            maternal_locator = None
        return maternal_locator

    @property
    def demographics_data(self):
        self.maternal_status_helper = MaternalStatusHelper(self.latest_visit)
        demographics_data = {}
        if self.antenatal_enrollment:
            if self.antenatal_enrollment.pending_ultrasound:
                demographics_data.update({'antenatal_enrollment_status': 'pending ultrasound'})
            elif self.antenatal_enrollment.is_eligible:
                demographics_data.update({'antenatal_enrollment_status': 'passed'})
            elif not self.antenatal_enrollment.is_eligible:
                demographics_data.update({'antenatal_enrollment_status': 'failed'})
            else:
                demographics_data.update({'antenatal_enrollment_status': 'Not filled'})
        demographics_data.update({'enrollment_hiv_status': self.maternal_status_helper.enrollment_hiv_status})
        demographics_data.update({'current_hiv_status': self.maternal_status_helper.hiv_status})
        demographics_data.update({'gestational_age': self.gestational_age})
        demographics_data.update({'delivery_site': self.delivery_site})
        demographics_data.update({'randomized': self.randomized})
        return demographics_data

    @property
    def latest_visit(self):
        return MaternalVisit.objects.filter(
            appointment__subject_identifier=self.subject_identifier).order_by(
                '-created').first()

    @property
    def consent(self):
        try:
            maternal_consent = MaternalConsent.objects.get(subject_identifier=self.subject_identifier)
        except MaternalConsent.DoesNotExist:
            maternal_consent = None
        return maternal_consent

    @property
    def show_forms(self):
        show = self.request.GET.get('show', None)
        return True if show == 'forms' else False

    @property
    def maternal_randomization(self):
        if not self.maternal_status_helper:
            self.maternal_status_helper = MaternalStatusHelper(self.latest_visit)
        try:
            maternal_rando = MaternalRando.objects.get(
                maternal_visit__appointment__subject_identifier=self.subject_identifier)
        except MaternalRando.DoesNotExist:
            maternal_rando = None
        return maternal_rando

    @property
    def maternal_delivery(self):
        if not self.maternal_status_helper:
            self.maternal_status_helper = MaternalStatusHelper(self.latest_visit)
        try:
            delivery = MaternalLabourDel.objects.get(
                registered_subject__subject_identifier=self.subject_identifier)
        except MaternalLabourDel.DoesNotExist:
            delivery = None
        return delivery

    @property
    def delivery_site(self):
        if self.maternal_delivery:
            return (self.maternal_delivery.delivery_hospital if
                    self.maternal_delivery.delivery_hospital != OTHER else
                    self.maternal_delivery.delivery_hospital_other)
        return UNK

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
    def gestational_age(self):
        if not self.maternal_status_helper:
            self.maternal_status_helper = MaternalStatusHelper(self.latest_visit)
        antenatal = self.antenatal_enrollment
        if antenatal:
            enrollment_helper = EnrollmentHelper(instance_antenatal=antenatal)
            if enrollment_helper.evaluate_ga_lmp(timezone.datetime.now().date()) and self.currently_pregnant:
                return enrollment_helper.evaluate_ga_lmp(timezone.datetime.now().date())
            elif ((not enrollment_helper.evaluate_ga_lmp(timezone.datetime.now().date()) and
                   self.currently_pregnant and antenatal.ultrasound)):
                return antenatal.ultrasound.ga_confirmed
            elif enrollment_helper.evaluate_ga_lmp(timezone.datetime.now().date()) and not self.currently_pregnant:
                delivery = self.maternal_delivery
                return enrollment_helper.evaluate_ga_lmp(delivery.delivery_datetime.date())
            else:
                return UNK
        return UNK

    @property
    def antenatal_enrollment(self):
        if not self.maternal_status_helper:
            self.maternal_status_helper = MaternalStatusHelper(self.latest_visit)
        try:
            antenatal_enrollment = AntenatalEnrollment.objects.get(
                registered_subject__subject_identifier=self.subject_identifier)
        except AntenatalEnrollment.DoesNotExist:
            antenatal_enrollment = None
        return antenatal_enrollment

    @property
    def randomized(self):
        try:
            randomization = MaternalRando.objects.get(
                maternal_visit__appointment__subject_identifier=self.subject_identifier)
            return randomization.rx
        except MaternalRando.DoesNotExist:
            return None

    @property
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
