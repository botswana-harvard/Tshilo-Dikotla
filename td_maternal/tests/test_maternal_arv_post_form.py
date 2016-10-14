from dateutil.relativedelta import relativedelta
from django.utils import timezone

from edc_constants.constants import (YES, NOT_APPLICABLE, POS, NO)

from td_appointment.models import Appointment
from td_registration.models import RegisteredSubject

from td_maternal.forms import MaternalArvPostForm

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, MaternalVisitFactory, MaternalLabourDelFactory, AntenatalVisitMembershipFactory)


class TestMaternalArvPost(BaseTestCase):

    def setUp(self):
        super(TestMaternalArvPost, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1010M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')

        MaternalLabourDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        self.maternal_visit_2000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.data = {
            'maternal_visit': self.maternal_visit_2000.id,
            'report_datetime': timezone.now(),
            'on_arv_since': NO,
            'on_arv_reason': 'N/A',
            'on_arv_reason_other': '',
            'arv_status': 'N/A'}

    def test_on_haart_1(self):
        """Assert that if mother was supposed to take HAART,
        then reason for haart cannot be N/A"""
        self.data['on_arv_since'] = YES
        form = MaternalArvPostForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("You indicated that participant was on triple ARVs. Reason CANNOT be"
                      " 'Not Applicable'. ", errors)

    def test_on_haart_2(self):
        """Assert that if mother was not supposed to take HAART, then cannot provide
        a reason for taking HAART"""
        self.data['on_arv_reason'] = 'pmtct bf'
        form = MaternalArvPostForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You indicated that participant was not on HAART. You CANNOT provide a reason.', errors)

    def test_on_haart_3(self):
        """Assert that mother was not supposed to take HAART and no reason for taking HAART
        is provided then valid"""
        form = MaternalArvPostForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_on_haart_4(self):
        """Assert that if mother was supposed to take HAART, and reason for HAART given is valid"""
        self.data['on_arv_since'] = YES
        self.data['on_arv_reason'] = 'pmtct bf'
        form = MaternalArvPostForm(data=self.data)
        self.assertTrue(form.is_valid())
