from collections import OrderedDict

from edc_registration.models import RegisteredSubject
from edc_base.utils import convert_from_camel
from edc_constants.constants import YES, POS, NEG, IND, NEVER, UNKNOWN, DWTA
from edc_dashboard.subject import RegisteredSubjectDashboard

from tshilo_dikotla.apps.td.constants import INFANT
from tshilo_dikotla.apps.td_lab.models import MaternalRequisition
from tshilo_dikotla.apps.td_maternal.models import (
    MaternalVisit, MaternalEligibility, MaternalConsent, MaternalLocator,
    AntenatalEnrollment)
from tshilo_dikotla.apps.td_infant.models import InfantBirth


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

    def get_context_data(self, **kwargs):
        super(MaternalDashboard, self).get_context_data(**kwargs)
#         postnatal_enrollment = self.postnatal_enrollment()
        antenatal_enrollment = self.antenatal_enrollment()
        self.context.update(
            home='tshilo_dikotla',
            search_name='maternal',
            title='Maternal Dashboard',
            subject_dashboard_url=self.subject_dashboard_url,
            infants=self.get_registered_infant_identifier(),
            maternal_consent=self.consent,
            local_results=self.render_labs(),
            antenatal_enrollment=self.antenatal_enrollment(),
#             postnatal_enrollment=postnatal_enrollment,
            antenatal_hiv_status=self.antenatal_maternal_hiv_status(antenatal_enrollment),
#             postnatal_hiv_status=self.postnatal_maternal_hiv_status(postnatal_enrollment),
        )
        return self.context

    @property
    def consent(self):
        self._consent = None
        try:
            self._consent = MaternalConsent.objects.filter(
                subject_identifier=self.subject_identifier).order_by('-version').first()
        except MaternalConsent.DoesNotExist:
            self._consent = None
        return self._consent

    def antenatal_maternal_hiv_status(self, antenatal_enrollment):
        maternal_hiv_status = None
        if antenatal_enrollment:
            if antenatal_enrollment.current_hiv_status == POS and antenatal_enrollment.evidence_hiv_status == YES:
                maternal_hiv_status = POS
            elif antenatal_enrollment.current_hiv_status == NEG and antenatal_enrollment.evidence_hiv_status == YES:
                maternal_hiv_status = NEG
            elif antenatal_enrollment.current_hiv_status == NEVER:
                maternal_hiv_status = 'Never Tested'
            elif antenatal_enrollment.current_hiv_status == UNKNOWN:
                maternal_hiv_status = 'UNK'
            elif antenatal_enrollment.current_hiv_status == DWTA:
                maternal_hiv_status = 'REFUSED'
            elif antenatal_enrollment.rapid_test_result == POS:
                maternal_hiv_status = 'POS ANT rapid test'
            elif antenatal_enrollment.rapid_test_result == NEG:
                maternal_hiv_status = 'NEG ANT rapid test'
            elif antenatal_enrollment.rapid_test_result == IND:
                maternal_hiv_status = 'IND ANT rapid test'
        return maternal_hiv_status

#     def postnatal_maternal_hiv_status(self, postnatal_enrollment):
#         maternal_hiv_status = None
#         if postnatal_enrollment:
#             if postnatal_enrollment.current_hiv_status == POS and postnatal_enrollment.evidence_hiv_status == YES:
#                 maternal_hiv_status = POS
#             elif postnatal_enrollment.current_hiv_status == NEG and postnatal_enrollment.evidence_hiv_status == YES:
#                 maternal_hiv_status = NEG
#             elif postnatal_enrollment.current_hiv_status == NEVER:
#                 maternal_hiv_status = 'Never Tested'
#             elif postnatal_enrollment.current_hiv_status == UNKNOWN:
#                 maternal_hiv_status = 'UNK'
#             elif postnatal_enrollment.current_hiv_status == DWTA:
#                 maternal_hiv_status = 'REFUSED'
#             elif postnatal_enrollment.rapid_test_result == POS:
#                 maternal_hiv_status = 'POS PNT rapid test'
#             elif postnatal_enrollment.rapid_test_result == NEG:
#                 maternal_hiv_status = 'NEG PNT rapid test'
#             elif postnatal_enrollment.rapid_test_result == IND:
#                 maternal_hiv_status = 'IND PNT rapid test'
#         return maternal_hiv_status

    def get_locator_scheduled_visit_code(self):
        """ Returns visit where the locator is scheduled, TODO: maybe search visit definition for this?."""
        return '1000M'

    @property
    def maternal_locator(self):
        return self.locator_model.objects.get(
            maternal_visit__appointment__registered_subject__subject_identifier=self.subject_identifier)

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
                dct['dashboard_id'] = convert_from_camel(infant_birth.pk)
                dct['dashboard_type'] = INFANT
                infants[infant_registered_subject.subject_identifier] = dct
            except InfantBirth.DoesNotExist:
                dct = {'subject_identifier': infant_registered_subject.subject_identifier}
                dct['dashboard_model'] = 'registered_subject'
                dct['dashboard_id'] = infant_registered_subject.pk
                dct['dashboard_type'] = INFANT
                infants[infant_registered_subject.subject_identifier] = dct
        except RegisteredSubject.DoesNotExist:
            pass
        return infants

    def antenatal_enrollment(self):
        try:
            antenatal_enrollment = AntenatalEnrollment.objects.get(registered_subject=self.registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            antenatal_enrollment = None
        return antenatal_enrollment

#     def postnatal_enrollment(self):
#         try:
#             postnatal_enrollment = PostnatalEnrollment.objects.get(registered_subject=self.registered_subject)
#         except PostnatalEnrollment.DoesNotExist:
#             postnatal_enrollment = None
#         return postnatal_enrollment
