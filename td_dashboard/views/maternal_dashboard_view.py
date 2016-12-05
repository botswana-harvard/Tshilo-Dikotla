from collections import OrderedDict

from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.utils import timezone

from edc_base.utils import convert_from_camel
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import UNK, OTHER
from edc_registration.models import RegisteredSubject

from td.constants import MATERNAL, INFANT
from td_infant.models.infant_birth import InfantBirth
from td_maternal.enrollment_helper import EnrollmentHelper
from td_maternal.maternal_hiv_status import MaternalHivStatus
from td_maternal.models import (
    AntenatalEnrollment, MaternalConsent, MaternalLabDel, MaternalLocator,
    MaternalRando, MaternalVisit)

from .mixins import DashboardMixin


class MaternalDashboardView(DashboardMixin, EdcBaseViewMixin, TemplateView):

    def __init__(self, **kwargs):
        super(MaternalDashboardView, self).__init__(**kwargs)
        self.request = None
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
            'td_maternal.antenatalvisitmembership', 'td_maternal.maternallabdel']

    def get_context_data(self, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
            site_header=admin.site.site_header,
        )
        self.context.update({
            'demographics': self.demographics,
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
            maternal_locator = MaternalLocator.objects.get(subject_identifier=self.subject_identifier)
        except MaternalLocator.DoesNotExist:
            maternal_locator = None
        return maternal_locator

    @property
    def demographics(self):
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.latest_visit.subject_identifier,
            reference_datetime=self.latest_visit.report_datetime)
        demographics = OrderedDict()
        if self.consent:
            demographics['Name'] = '{}({})'.format(self.consent.first_name, self.consent.initials),
            demographics['Born'] = self.consent.dob,
            demographics['Age'] = self.age,
            demographics['Consented'] = self.consent.consent_datetime,
            demographics['Antenatal enrollment status'] = maternal_hiv_status.enrollment_hiv_status,
            demographics['Enrollment HIV status'] = maternal_hiv_status.enrollment_hiv_status,
            demographics['Current HIV status'] = maternal_hiv_status.result,
            demographics['Pregnant, GA'] = self.gestational_age,
            demographics['Planned delivery site'] = self.delivery_site,
            demographics['Randomized'] = (self.randomized,)
        return demographics

    @property
    def antenatal_enrollment_status(self):
        if self.antenatal_enrollment:
            if self.antenatal_enrollment.ga_pending and self.antenatal_enrollment.is_eligible:
                antenatal_enrollment_status = 'Pending ultrasound'
            elif self.antenatal_enrollment.is_eligible:
                antenatal_enrollment_status = 'Passed'
            elif not self.antenatal_enrollment.is_eligible:
                antenatal_enrollment_status = 'Failed'
            else:
                antenatal_enrollment_status = 'Not filled'
        return antenatal_enrollment_status

    @property
    def latest_visit(self):
        return MaternalVisit.objects.filter(
            subject_identifier=self.subject_identifier).order_by('-report_datetime').first()

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
    def maternal_rando(self):
        try:
            maternal_rando = MaternalRando.objects.get(
                maternal_visit__subject_identifier=self.subject_identifier)
        except MaternalRando.DoesNotExist:
            maternal_rando = None
        return maternal_rando

    @property
    def maternal_delivery(self):
        try:
            delivery = MaternalLabDel.objects.get(
                registered_subject__subject_identifier=self.subject_identifier)
        except MaternalLabDel.DoesNotExist:
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
        if self.maternal_rando and self.maternal_rando.delivery_clinic != OTHER:
            return self.maternal_rando.delivery_clinic
        elif self.maternal_rando and self.maternal_rando.delivery_clinic == OTHER:
            return self.maternal_rando.delivery_clinic_other
        else:
            return UNK

    @property
    def gestational_age(self):
        antenatal = self.antenatal_enrollment
        if antenatal:
            enrollment_helper = EnrollmentHelper(antenatal)
            if enrollment_helper.get_ga_lmp_enrollment_wks(timezone.datetime.now().date()) and self.currently_pregnant:
                return enrollment_helper.get_ga_lmp_enrollment_wks(timezone.datetime.now().date())
            elif ((not enrollment_helper.get_ga_lmp_enrollment_wks(timezone.datetime.now().date()) and
                   self.currently_pregnant and antenatal.ultrasound)):
                return antenatal.ultrasound.ga_confirmed
            elif enrollment_helper.get_ga_lmp_enrollment_wks(timezone.datetime.now().date()) and not self.currently_pregnant:
                delivery = self.maternal_delivery
                return enrollment_helper.get_ga_lmp_enrollment_wks(delivery.delivery_datetime.date())
            else:
                return UNK
        return UNK

    @property
    def antenatal_enrollment(self):
        try:
            antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        except AntenatalEnrollment.DoesNotExist:
            antenatal_enrollment = None
        return antenatal_enrollment

    @property
    def randomized(self):
        try:
            randomization = MaternalRando.objects.get(maternal_visit__subject_identifier=self.subject_identifier)
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
