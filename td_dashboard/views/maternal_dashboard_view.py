from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

from edc_base.views import EdcBaseViewMixin
from ..classes import MarqueeViewMixin, AppointmentSubjectVisitCRFViewMixin, LocatorResultsActionsViewMixin
from td_maternal.models.maternal_consent import MaternalConsent
from td_maternal.models.requisition_meta_data import RequisitionMetadata
from edc_constants.constants import UNK, OTHER
from td_maternal.models.maternal_locator import MaternalLocator
from td_maternal.models.maternal_crf_meta_data import CrfMetadata
from tshilo_dikotla.constants import MATERNAL
from td_maternal.models.antenatal_enrollment import AntenatalEnrollment
from td_maternal.models.maternal_visit import MaternalVisit
from td_maternal.classes.maternal_status_helper import MaternalStatusHelper
from td_maternal.models.enrollment_helper import EnrollmentHelper
from django.utils import timezone
from td_maternal.models.maternal_labour_del import MaternalLabourDel
from td_maternal.models.maternal_randomization import MaternalRando


class MaternalDashboardView(
        MarqueeViewMixin,
        AppointmentSubjectVisitCRFViewMixin, LocatorResultsActionsViewMixin, EdcBaseViewMixin, TemplateView):

    def __init__(self, **kwargs):
        super(MaternalDashboardView, self).__init__(**kwargs)
        self.request = None
        self.context = {}
        self.show = None
        self.maternal_status_helper = None
        self.template_name = 'td_dashboard/subject_dashboard.html'
        self.membership_form_category = [
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
            'marquee_data': self.marquee_data.items(),
            'markey_next_row': self.markey_next_row,
            'requistions_metadata': self.requistions_metadata,
            'scheduled_forms': self.scheduled_forms[0],
            'visit_code': self.scheduled_forms[1],
            'appointments': self.appointments,
            'subject_identifier': self.subject_identifier,
            'consents': [],
            'dashboard_type': MATERNAL,
            'locator': self.locator,
            'subject_membership_models': self.subject_membership_models()
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
    def maternal_marquee_data(self):
        self.maternal_status_helper = MaternalStatusHelper(self.latest_visit)
        maternal_marquee_data = {}
        if self.antenatal_enrollment:
            if self.antenatal_enrollment.pending_ultrasound:
                maternal_marquee_data.update({'antenatal_enrollment_status': 'pending ultrasound'})
            elif self.antenatal_enrollment.is_eligible:
                maternal_marquee_data.update({'antenatal_enrollment_status': 'passed'})
            elif not self.antenatal_enrollment.is_eligible:
                maternal_marquee_data.update({'antenatal_enrollment_status': 'failed'})
            else:
                maternal_marquee_data.update({'antenatal_enrollment_status': 'Not filled'})
        maternal_marquee_data.update({'enrollment_hiv_status': self.maternal_status_helper.enrollment_hiv_status})
        maternal_marquee_data.update({'current_hiv_status': self.maternal_status_helper.hiv_status})
        maternal_marquee_data.update({'gestational_age': self.gestational_age})
        maternal_marquee_data.update({'delivery_site': self.delivery_site})
        maternal_marquee_data.update({'randomized': self.randomized})
        return maternal_marquee_data

    @property
    def scheduled_forms(self):
        visit_code = self.appointment.visit_code if self.appointment else '1000M'
        scheduled_forms = CrfMetadata.objects.filter(
            subject_identifier=self.subject_identifier,
            visit_code=visit_code).order_by('created')
        return (scheduled_forms, visit_code)

    @property
    def requistions_metadata(self):
        visit_code = self.appointment.visit_code if self.appointment else '1000M'
        requistions_metadata = RequisitionMetadata.objects.filter(
            subject_identifier=self.subject_identifier,
            visit_code=visit_code
        )
        return requistions_metadata

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
    def subject_identifier(self):
        return self.context.get('subject_identifier')

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
            elif (not enrollment_helper.evaluate_ga_lmp(timezone.datetime.now().date()) and self.currently_pregnant
                  and antenatal.ultrasound):
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
